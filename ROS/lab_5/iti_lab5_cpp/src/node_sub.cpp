#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/int64.hpp"
#include <chrono>
#include <string>

class Node2: public rclcpp::Node
{
    public:
    Node2():Node("Node2")
    {
        RCLCPP_WARN(this->get_logger(),"Subscriber is starting now");
        string_subscriber = this->create_subscription<std_msgs::msg::String>("str_topic",rclcpp::SensorDataQoS(),std::bind(&Node2::listener, this, std::placeholders::_1));
    }

    private:
    void listener(const std_msgs::msg::String::SharedPtr msg)const
    {
        RCLCPP_INFO(this->get_logger(),msg->data.c_str());
    }
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr string_subscriber;

};

int main(int argc, char * argv[] )
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Node2>());
    rclcpp::shutdown();
    return 0;
}