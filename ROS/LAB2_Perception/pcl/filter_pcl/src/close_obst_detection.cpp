#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "carkyo_msgs/msg/camera_emergency.hpp"
#include <pcl_conversions/pcl_conversions.h>
// Ransac includes
#include "filter_pcl/processPointClouds.h"
#include "processPointClouds.cpp"

 
using namespace std;

class PointcloudFilter : public rclcpp::Node
{
  public:
    std::string ip_Topic_name_cropped = "" ;
    std::string op_Topic_name = "" ;
    
    PointcloudFilter()
    : Node("close_obst_detection_node")
    {
      this->declare_parameter<std::string>("ip_Topic_name", "/intel/cropped");
      this->declare_parameter<std::string>("op_Topic_name", "/cameraEmergency");

      this->get_parameter("ip_Topic_name", ip_Topic_name_cropped);
      this->get_parameter("op_Topic_name", op_Topic_name);
         
            
      RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "create sub");
      subscriber_ = this->create_subscription<sensor_msgs::msg::PointCloud2>(ip_Topic_name_cropped, 5, std::bind(&PointcloudFilter::subscribe_message, this, std::placeholders::_1));
      publisher_camera_emergency = this->create_publisher<carkyo_msgs::msg::CameraEmergency>(op_Topic_name, 10);

    }

  private:

    void subscribe_message(const sensor_msgs::msg::PointCloud2::SharedPtr message) const
    {
        int len_data = message->data.size();
        //RCLCPP_INFO(this->get_logger(),std::to_string(len_data));
        // Conversion to PCL
	      pcl::PCLPointCloud2 pcl_pc2;
	      pcl_conversions::toPCL(*message,pcl_pc2);
	      pcl::PointCloud<pcl::PointXYZ>::Ptr inputCloudI(new pcl::PointCloud<pcl::PointXYZ>);
	      pcl::fromPCLPointCloud2(pcl_pc2,*inputCloudI);
      
        float smallest_val = std::numeric_limits<float>::max();
        for (size_t i = 0; i < inputCloudI->points.size(); i++){
            //float x = inputCloudI->points[i].x;
            //float y = inputCloudI->points[i].y;
            float z = inputCloudI->points[i].z;
            if(z<smallest_val){
           smallest_val = z;}
           RCLCPP_INFO(this->get_logger(),std::to_string(smallest_val));
           
            // x is right and left , + is left
            // z is forward and back , + is forward (all data should be + , close obst should be 0:1m)
            // y is down and up , +ve is down, ground obst should be > 0.1
            //if (z < 1 &&  y < 0.1)    // Another way to filter without using processpointclouf file        
        }
        
        carkyo_msgs::msg::CameraEmergency emergency_msg = carkyo_msgs::msg::CameraEmergency();
        if (len_data>0)
        {
            emergency_msg.close_obstacle_detected = true;
            emergency_msg.min_distance = smallest_val;
        }
        else
        {
            emergency_msg.close_obstacle_detected = false;
        } 
        
        RCLCPP_INFO(this->get_logger(),std::to_string(len_data));
        RCLCPP_INFO(this->get_logger(),std::to_string(emergency_msg.close_obstacle_detected));
        RCLCPP_INFO(this->get_logger(),std::to_string(emergency_msg.min_distance));
        
        publisher_camera_emergency->publish(emergency_msg);

    }
    rclcpp::Node::SharedPtr nh_;
    rclcpp::Publisher<carkyo_msgs::msg::CameraEmergency>::SharedPtr publisher_camera_emergency;
    rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscriber_;
};

int main(int argc, char * argv[])
{
  RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Ready");
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PointcloudFilter>());
  rclcpp::shutdown();
  return 0;
}
