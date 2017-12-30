
def compute_cost(storage, convert_to_video=False):

    # raw screenshots
    # actually more like 200-300 KB on my laptop
        # but are those half-size?
    mb_per_image = 1.
    if(convert_to_video):
        mb_per_image *= .3

    # number of days to store
    num_days = 365

    cost_per_gb_per_month = {'s3':.0125, 'glacier':.004}[storage]

    # 1 image / 5 seconds * 60 seconds * 60 minutes * 8 hours
    images_per_day = 1. / 10 * 60 * 60 * 24  # 8640 images per day
    print 'storing {} images per day on {} {}'.format(
        int(round(images_per_day)), storage,
        'in video format' if convert_to_video else '')

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
compute_cost('s3', convert_to_video=True)
print
compute_cost('glacier', convert_to_video=True)
print

