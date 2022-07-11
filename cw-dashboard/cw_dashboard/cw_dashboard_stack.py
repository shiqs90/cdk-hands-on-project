from aws_cdk import (
    Stack,
    aws_elasticloadbalancingv2 as elbv2,
    aws_cloudwatch as cw
)
from constructs import Construct

class CwDashboardStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #load_balancer = elbv2.ApplicationLoadBalancer.from_application_load_balancer_attributes(
            #self,
            #"ALB",
            #load_balancer_arn="arn:aws:elasticloadbalancing:ap-south-1:345396902820:loadbalancer/app/QA-Env-Public-ALB/573f88222ed64875",
            #security_group_id="sg-0d4c3f7da30c146d6"
        #)
        load_balancer = elbv2.ApplicationLoadBalancer.from_lookup(
            self,
            "ALB",
            load_balancer_arn="arn:aws:elasticloadbalancing:ap-south-1:345396902820:loadbalancer/app/QA-Env-Public-ALB/573f88222ed64875"
        )        
        print(load_balancer)
        http_5xx_metric = load_balancer.metric_http_code_elb(
            code=elbv2.HttpCodeElb.ELB_5XX_COUNT
        )

        http_requests_metric = load_balancer.metric_request_count(
            statistic="SUM"
        )

        http_response_times = load_balancer.metric_target_response_time()

        load_balancer_widget = cw.GraphWidget(
            title="Load Balancer Metrics",
            height=8,
            width=12,
            left=[http_5xx_metric],
            right=[http_requests_metric]
        )

        http_response_widget = cw.GraphWidget(
            title="Response Times",
            height=8,
            width=12,
            left=[http_response_times]
        )

        cw.Dashboard(
            self,
            "Dashboard",
            dashboard_name="Service-Status",
            widgets=[
                [load_balancer_widget, http_response_widget]
            ]
        )
