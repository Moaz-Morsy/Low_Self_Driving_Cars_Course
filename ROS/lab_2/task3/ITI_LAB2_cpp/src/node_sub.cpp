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
        //str_publisher = this->create_publisher<std_msgs::msg::String>("int_fb",10);
        int_publisher = this->create_publisher<std_msgs::msg::Int64>("int_fb",10);
        string_subscriber = this->create_subscription<std_msgs::msg::String>("str_topic",10,std::bind(&Node2::listener, this, std::placeholders::_1));
    }

    private:
    void listener(const std_msgs::msg::String::SharedPtr msg)const
    {
        std::string s = msg->data.c_str();
        size_t i = 0;
        //unsigned int i = 0;
        for ( ; i < s.length(); i++ ){ if ( isdigit(s[i]) ) break; }
        s = s.substr(i, s.length() - i );
        //std_msgs::msg::String string_msg = std_msgs::msg::String();
        std_msgs::msg::Int64 num_msg = std_msgs::msg::Int64(); 
        //string_msg.data = s;
        num_msg.data = std::stoi(s);
        int_publisher->publish(num_msg);
    }
    //rclcpp::Publisher<std_msgs::msg::String>::SharedPtr str_publisher;
    rclcpp::Publisher<std_msgs::msg::Int64>::SharedPtr int_publisher;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr string_subscriber;

};

int main(int argc, char * argv[] )
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Node2>());
    rclcpp::shutdown();
    return 0;
}