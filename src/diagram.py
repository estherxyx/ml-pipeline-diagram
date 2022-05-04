from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.compute import Fargate
from diagrams.aws.general import User
from diagrams.aws.iot import IotCar

node_attr = {
    "fontsize": "10"
}

graph_attr = {
    "bgcolor": "transparent"
}

with Diagram(
        name="ML Pipeline Diagram: Application Cross Validation Workflow",
        outformat="png",
        filename="output",
        show=False,
        node_attr=node_attr,
        graph_attr=graph_attr):
    input = User("RS/PM")
    with Cluster("Data Processing Flow"):
        dp_entry = S3("Raw Data Input")

        with Cluster("Applications"):
            software = [
                Fargate("App-A"),
                Fargate("App-B"),
                Fargate("App-C")
            ]

        with Cluster("Outputs"):
            dp_exit = [
                S3(app.label+"-Output") for app in software
            ]

        dp_entry >> Lambda("Input Normalization\n Handler") >> software
        for i in range(len(software)):
            software[i] >> dp_exit[i]


    with Cluster("Output Normalization Flow"):
        mi_entry = Lambda("Output Normalization\n Handler")
        mi_exit = S3("Normalized Output")
        mi_entry >> mi_exit

    with Cluster("Ground Truth Flow"):
        vf_entry = IotCar("IoT")
        vf_exit = S3("Real World Output")
        vf_entry >> vf_exit

    output = User("RS")

    input >> dp_entry
    dp_exit >> mi_entry
    input >> vf_entry
    mi_exit >> output
    vf_exit >> output