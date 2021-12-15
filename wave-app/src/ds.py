from h2o_wave import main, app, Q, ui, on, data
import pandas as pd

# Data prep step from the submission notebook (challenge_wildfires/notebook/).
async def get_data(q:Q, path:str):

    aus_fires = pd.read_csv(path, parse_dates=['acq_date'])
    aus_fires['year'] = aus_fires.acq_date.dt.year
    aus_fires['month'] = aus_fires.acq_date.dt.month
    aus_fires['day'] = aus_fires.acq_date.dt.day

    aus_fires['est_fire_area'] = aus_fires['scan'] * aus_fires['track']
    aus_fires['est_brightness'] = (aus_fires['brightness'] + aus_fires['bright_t31']) / 2
    aus_fires.latitude = aus_fires.latitude.round(1)
    aus_fires.longitude = aus_fires.longitude.round(1)

    fires = aus_fires[['latitude', 'longitude', 'year', 'month', 'day', 'confidence',
                       'est_fire_area', 'est_brightness', 'frp', 'type', 'daynight']].copy()

    count = fires.groupby(['latitude', 'longitude', 'year', 'month', 'day']).size().reset_index().rename(
        columns={0: 'fire_count'})
    fire_copy = fires.merge(count, how='outer', on=['latitude', 'longitude', 'year', 'month', 'day'])

    def fire_happend(fire_copy):  # here fire_copy == row
        if ((fire_copy['confidence'] >= 70) & (fire_copy['fire_count'] > 1) & (fire_copy['type'] == 0)):
            return 4
        elif ((fire_copy['confidence'] >= 70) & (fire_copy['fire_count'] == 1) & (fire_copy['type'] == 0)):
            return 3
        elif ((fire_copy['confidence'] < 70) & (fire_copy['confidence'] >= 40) & (fire_copy['fire_count'] > 1) & (
                fire_copy['type'] == 0)):
            return 3
        elif ((fire_copy['confidence'] < 70) & (fire_copy['confidence'] >= 40) & (fire_copy['fire_count'] == 1) & (
                fire_copy['type'] == 0)):
            return 2
        elif ((fire_copy['confidence'] < 40) & (fire_copy['confidence'] >= 0) & (fire_copy['fire_count'] > 1) & (
                fire_copy['type'] == 0)):
            return 2
        elif ((fire_copy['confidence'] < 40) & (fire_copy['confidence'] >= 0) & (fire_copy['fire_count'] == 1) & (
                fire_copy['type'] == 0)):
            return 1
        else:
            return 0

    fire_copy['est_fire_happend'] = fire_copy.apply(lambda row: fire_happend(row), axis=1)

    fire_copy = fire_copy.groupby(['latitude', 'longitude', 'year', 'month', 'day'])[
        ['fire_count', 'confidence', 'frp', 'est_fire_area', 'est_brightness', 'est_fire_happend']].mean().reset_index()

    fire_copy.est_fire_happend = fire_copy.est_fire_happend.round().astype(int)
    fire_copy.est_fire_area = fire_copy.est_fire_area.round(1)
    fire_copy.est_brightness = fire_copy.est_brightness.round(1)
    fire_copy.confidence = fire_copy.confidence.round().astype(int)
    fire_copy.frp = fire_copy.frp.round(1)
    fire_copy.fire_count = fire_copy.fire_count.round().astype(int)

    fire_copy = fire_copy.sort_values(by=['latitude', 'longitude'])


    features = [
        'latitude', 'longitude', 'year', 'month', 'day',
        'est_fire_area', 'est_brightness', 'frp', 'fire_count',
        'confidence'
    ]
    
    return (fire_copy, features)
