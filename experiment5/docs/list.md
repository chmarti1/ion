# List.py

Because the data set is so large, it is necessary to have tools to quickly visualize their contents.  The `list.py` script prints a table listing each horizontal scan dataset with the date and time it was collected, its `z` (height), the number of files in the dataset, and a list of the post-processing steps that are found.

Below is an example output of `list.py`.

```python
$ cd bin
$ ./list.py
Feb 24 2020 17:08:14  z=9.0mm [19] post:16
Feb 24 2020 17:04:05  z=9.5mm [15] post:16
Feb 24 2020 16:57:13  z=9.5mm [15] post:16
Feb 24 2020 16:53:57  z=9.5mm [15] post:16
Feb 24 2020 16:49:29  z=9.5mm [15] post:16
Feb 24 2020 16:41:40  z=9.5mm [15] post:16
Feb 24 2020 16:34:12  z=9.5mm [15] post:16
Feb 24 2020 16:29:49  z=4.0mm [2] post:
Feb 24 2020 14:16:15  z=2.0mm [9] post:
Feb 17 2020 16:57:42  z=7.0mm [162] post:123
Feb 17 2020 16:47:54  z=9.0mm [162] post:123
Feb 17 2020 16:37:38  z=10.0mm [162] post:123
Feb 17 2020 16:27:16  z=8.0mm [162] post:123
Feb 17 2020 16:13:02  z=6.0mm [162] post:123
Feb 17 2020 16:03:06  z=4.0mm [162] post:123
Feb  3 2020 17:44:33  z=4.0mm [162] post:123
Feb  3 2020 17:34:46  z=6.0mm [162] post:123
Feb  3 2020 17:25:16  z=8.0mm [162] post:123
Feb  3 2020 17:15:32  z=7.0mm [162] post:123
Feb  3 2020 17:05:53  z=5.0mm [162] post:123
Feb  3 2020 16:55:59  z=3.0mm [162] post:123
Jan 27 2020 17:08:32  z=6.0mm [162] post:123
Jan 27 2020 16:58:41  z=8.0mm [162] post:123
Jan 27 2020 16:49:17  z=9.0mm [162] post:123
Jan 27 2020 16:39:18  z=7.0mm [162] post:123
Jan 27 2020 16:29:43  z=5.0mm [162] post:123
Jan 27 2020 16:20:24  z=4.0mm [162] post:123
Jan 27 2020 16:14:32  z=4.0mm [45] post:
Jan 16 2020  0:00:01  z=3.0mm [9] post:15
Jan 16 2020  0:00:00  z=3.0mm [18] post:
Jan 15 2020  0:00:00  z=3.0mm [14] post:5
Dec  5 2019 10:33:25  z=1.5mm [162] post:123
Dec  5 2019 10:24:13  z=2.5mm [162] post:123
Dec  5 2019 10:14:42  z=3.5mm [162] post:123
Dec  5 2019 10:05:14  z=4.0mm [162] post:123
Dec  5 2019  9:55:42  z=3.0mm [162] post:123
Dec  5 2019  9:46:30  z=2.0mm [162] post:123
Dec  5 2019  9:37:06  z=1.0mm [162] post:123
Dec  2 2019 11:28:43  z=4.0mm [49] post:
Dec  2 2019 11:19:02  z=3.0mm [162] post:
Dec  2 2019 11:09:33  z=2.0mm [162] post:
Dec  2 2019 10:58:07  z=1.0mm [162] post:
Nov 26 2019 14:50:43  z=3.0mm [162] post:123
Nov 26 2019 14:39:29  z=3.0mm [162] post:123
Nov 26 2019 14:28:19  z=3.0mm [162] post:123
Nov 20 2019 17:08:49  z=4.5mm [162] post:123
Nov 20 2019 16:59:24  z=6.0mm [162] post:123
Nov 20 2019 16:49:28  z=3.0mm [162] post:123
Nov 20 2019 16:39:22  z=1.5mm [162] post:123
Nov 20 2019 16:24:31  z=1.5mm [162] post:123
Nov 11 2019 11:41:17  z=7.5mm [162] post:123
Nov 11 2019 11:32:05  z=4.5mm [162] post:123
Nov 11 2019 11:22:21  z=6.0mm [162] post:123
Nov 11 2019 11:10:42  z=3.0mm [162] post:123
Nov  4 2019 14:07:56  z=0.0mm [162] post:123
Oct 16 2019  8:47:13  [100] post:12
Oct 14 2019 14:24:30  [100] post:1
```