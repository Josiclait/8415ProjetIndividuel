import boto3

ec2_client = boto3.client("ec2", region_name="us-east-1")

def createInstance(name, privateIp, SecurityGroupId, userData, InstanceType = "t2.micro"):
    """
    Create an instance from the params passed

    :param: name of the instance to create
    :param: privateIp of the instance to create
    :param: SecurityGroupId of the instance to create
    :param: userData of the instance to create
    :param: InstanceType of the instance to create
    :return the instance created
    """
    return ec2_client.run_instances(
        ImageId="ami-0a6b2839d44d781b2",
        MinCount=1,
        MaxCount=1,
        InstanceType=InstanceType,
        KeyName="vockey",
        UserData=userData,
        SecurityGroupIds=[SecurityGroupId],
        SubnetId='subnet-0d6af2ce628f6f9e2',
        PrivateIpAddress=privateIp,
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': name
                },
            ]
        },
        ]
    )


if __name__ == "__main__":
    ec2 = boto3.client("ec2", region_name="us-east-1")

    # Creating a security group for the gatekeeper
    gatekeeper_sg = ec2.create_security_group(
            GroupName='gatekeeper',
            Description='private-security-group'
        )

    # Creating a secure security group
    secure_sg = ec2.create_security_group(
            GroupName='secure',
            Description='security-group for sql cluster'
        )

    # Authorizing all communication in the virtual private cloud
    ec2.authorize_security_group_ingress(
            GroupName='secure',
            CidrIp="172.31.0.0/20",
            IpProtocol='-1',
            FromPort=0,
            ToPort=65535,
        )

    # Creating stand-alone
    master = ec2_client.run_instances(
        ImageId="ami-0a6b2839d44d781b2",
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName="vockey",
    )

    # Creating master
    master = ec2_client.run_instances(
        ImageId="ami-0a6b2839d44d781b2",
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName="vockey",
        SecurityGroupIds=[secure_sg['GroupId']],
    )

    # Creating slaves 
    slaves = ec2_client.run_instances(
        ImageId="ami-0a6b2839d44d781b2",
        MinCount=3,
        MaxCount=3,
        InstanceType='t2.micro',
        KeyName="vockey",
        SecurityGroupIds=[secure_sg['GroupId']],
    )
    
    # Creating proxy 
    proxy = ec2_client.run_instances(
        ImageId="ami-0a6b2839d44d781b2",
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.large',
        KeyName="vockey",
        SecurityGroupIds=[secure_sg['GroupId']],
    )

    # Creating gatekeeper 
    gatekeeper = ec2_client.run_instances(
        ImageId="ami-0a6b2839d44d781b2",
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.large',
        KeyName="vockey",
        SecurityGroupIds=[gatekeeper_sg['GroupId']],
    )

    # Creating trusted host 
    gatekeeper = ec2_client.run_instances(
        ImageId="ami-0a6b2839d44d781b2",
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.large',
        KeyName="vockey",
        SecurityGroupIds=[gatekeeper_sg['GroupId']],
    )


