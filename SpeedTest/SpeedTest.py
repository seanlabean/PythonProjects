import pyspeedtest
import schedule
import time

def test():
    """
    stackoverflow.com/questions/48289636
    """
    s = pyspeedtest.SpeedTest()
    res = {'download':0.0,
          'upload':0.0,
          'ping':0.0}
    res['download'] = s.download()
    res['upload'] = s.upload()
    return res["download"], res["upload"]

def write_txt():
    """

    """
    d_sum = 0.0
    u_sum = 0.0
    with open('speed.txt', 'a+') as f:
        for i in range(3):
            d, u = test()
            d_sum += d
            u_sum += u
        d_avg = d_sum/3
        u_avg = u_sum/3
        f.write('{:.2f}, {:.2f}\n'.format(d_avg/(1024*1024), u_avg/(1024*1024)))


def main():
    """
    stackoverflow.com/questions/15088037
    """
    schedule.every().day.at("14:20").do(write_txt(),'It is 01:00')

    while True:
        schedule.run_pending()
        time.sleep(60) # wait one minute


if __name__ == '__main__':
    main()
