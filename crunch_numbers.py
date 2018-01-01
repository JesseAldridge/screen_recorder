
import config

def compute_cost(storage, compressed=False):

    # raw screenshots
    # actually more like 200-300 KB on my laptop
        # but are those half-size?
    mb_per_image = 1.
    if(compressed):
        mb_per_image *= .3

    # number of days to store
    num_days = 365

    cost_per_gb_per_month = {'s3':.0245, 'glacier':.004}[storage]

    # 1 image / 10 seconds * 60 seconds * 60 minutes * 16 hours
    images_per_day = 1. / config.config_dict['secs_per_shot'] * 60 * 60 * 16  # ~6K images per day
    print 'storing {} images per day on {} {}'.format(
        int(round(images_per_day)), storage,
        'in compressed format' if compressed else '')

    gb_per_day = mb_per_image / 1000. * images_per_day
    print 'gb per year: ', gb_per_day * 30 * 12

    total_cost, total_gb = 0, 0
    for day in range(366):
        if day < num_days:
            total_gb += gb_per_day
        daily_cost = (cost_per_gb_per_month / 30.) * total_gb
        total_cost += daily_cost

        if day not in [30, 365]:
            continue
        s = ('after {day} days I will be using {total_gb:.0f} GB, will have '
             'spent ${total_cost:.0f}, and daily cost will be '
             '${daily_cost:.2f}').format(
             **locals())
        print s.format(day, total_cost)

compute_cost('glacier')
print
compute_cost('s3')
print
compute_cost('s3', compressed=True)
print
compute_cost('glacier', compressed=True)
print

