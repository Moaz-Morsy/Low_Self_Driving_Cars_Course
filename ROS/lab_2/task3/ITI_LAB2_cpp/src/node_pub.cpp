#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/int64.hpp"
#include <chrono>
#include <string>

class Node1: public rclcpp::Node
{
    public:
    Node1():Node("Node1")
    {
        RCLCPP_WARN(this->get_logger(),"Publisher is starting now");
        string_publisher = this->create_publisher<std_msgs::msg::String>("str_topic",10);
        timer = this->create_wall_timer(std::chrono::milliseconds(1000), std::bind(&Node1::timer_cb,this));
    }

    private:
    void timer_cb()
    {
        std_msgs::msg::String string_msg = std_msgs::msg::String();
        string_msg.data = "Moaz is publishing: " + std::to_string(x);
        x++;
        string_publisher->publish(string_msg);
    }
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr string_publisher;
    rclcpp::TimerBase::SharedPtr timer;
    int x=0;

};

int main(int argc, char * argv[] )
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Node1>());
    rclcpp::shutdown();
    return 0;
}