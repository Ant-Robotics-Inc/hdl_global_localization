# map_relocalistion
The ROS node for working with hdl_global_localization


#### Subscribed Topics:
 global_map ([sensor_msgs/PointCloud2](http://docs.ros.org/api/sensor_msgs/html/msg/PointCloud2.html)): Topic of global map.<br/>
 /lio_sam/mapping/map_local ([sensor_msgs/PointCloud2](http://docs.ros.org/api/sensor_msgs/html/msg/PointCloud2.html)): Topic of current map.<br/>
 
 Publisher Topics:

tf2 ([geometry_msgs/TransformStamped](http://docs.ros.org/api/geometry_msgs/html/msg/TransformStamped.html)): Tf2 publish frames: frame_id -> child_id <br/> 

#### Services:

relocalize ([std_srvs/Trigger](http://docs.ros.org/en/api/std_srvs/html/srv/Trigger.html): Service to manually run relocalization. <br/> 


#### Parameters:

~rate (float, default: 100)<br/>
&emsp;&emsp;*Frame rate of TF publiser<br/>*
~frame_id (string, default: "map")<br/>
&emsp;&emsp;*Name of parent TF.<br/>*
~child_id (string, default: "map_slam")<br/>
&emsp;&emsp;*frame of child TF.<br/>*

# hdl_global_localization

![hdl_global_localization](https://user-images.githubusercontent.com/31344317/105116113-71fc6180-5b0d-11eb-9d85-bbea922dde84.gif)

[![Build Status](https://travis-ci.org/koide3/hdl_global_localization.svg?branch=master)](https://travis-ci.org/koide3/hdl_global_localization) on ROS melodic and noetic

## Install deps

[!Teaser++](https://teaser.readthedocs.io/en/master/installation.html#supported-platforms)


## BUILD
added in ~/.bashrc

```
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/
```

## Requirements
***hdl_global_localization*** requires the following libraries:
- PCL
- OpenCV
- OpenMP
- Teaser++ [optional]

## Services

- ***/hdl_global_localization/set_engine*** (hdl_global_localization::SetGlobalLocalizationEngine)
  - Available global localization engines: BBS, FPFH_RANSAC, FPFH_TEASER
- ***/hdl_global_localization/set_global_map*** (hdl_global_localization::SetGlobalMap)
- ***/hdl_global_localization/query*** (hdl_global_localization::QueryGlobalLocalization)


## Algorithms

- 2D Grid Map-based Branch-and-Bound Search
  - Real-time loop closure in 2D LIDAR SLAM, ICRA, 2016
- FPFH + RANSAC (based on pcl::SampleConsensusPrerejective)
  - Fast Point Feature Histograms (FPFH) for 3D registration, ICRA, 2009
  - Pose Estimation using Local Structure-Specific Shape and Appearance Context, ICRA, 2013
- FPFH + Teaser++
  - TEASER: Fast and Certifiable Point Cloud Registration, T-RO, 2020

## Related packages

- [interactive_slam](https://github.com/koide3/interactive_slam)
- [hdl_graph_slam](https://github.com/koide3/hdl_graph_slam)
- [hdl_localization](https://github.com/koide3/hdl_localization">hdl_localization)
- [hdl_people_tracking](https://github.com/koide3/hdl_people_tracking">hdl_people_tracking)

## Contact
Kenji Koide, k.koide@aist.go.jp

Human-Centered Mobility Research Center, National Institute of Advanced Industrial Science and Technology (AIST), Japan
