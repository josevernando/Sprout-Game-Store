class Developer extends Account 
{
    constructor(developer_id, devName, devGameList) 
    {
        this.developer_id = developer_id;
        this.devName = devName;
        this.devGameList = devGameList;
    }

    requestPublishGame(){};
    publishGame(){};
}