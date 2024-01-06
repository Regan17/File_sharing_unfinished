Hey there, this is my approach towards building a file sharing system between an operational user and a client user.
    Firstly i designed basic frontend for my login signup and all views for the end user to look interesting.
    Main focus was on functionalities like differentiating between a client and operation user so for that i added a check box in the sign up page for the user tp say whether he wants to be a client user or a operation user.
    This made all the functioanlities different for both the users after signing up as for ops user after authentication, adifferent web page will open while another one for the client with different functionalities.
    Also,I made use of Django Rest Framework to upload files using APIs and authorization was also done using JSON tokens and is also shown in a picture below which helps the operational user to upload a file if he is authenticated.
    I was stuck at a point where my front end was not responding to the upload file request and was showing file upload was not succesful because of some error which i need to find out.
    After that thing was done, I already had the download part figured out for the client user and only a page for client user is to be made and these buttons needed to be added to download the file and a list of all files.
    For testing I can do unit and integration tests after completion of the project.I have also attached an example of tests.py for my code at last.
    For linting, I can use Flake8 and black to get code according to PEP8 standards.
    For deployment into production i can use Docker to create and image and then use AWS service named ECS to make a task defination to run this image in an ECS cluster.
    This will be achieved easily and without any problem; only code completion will be done first.
    
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/805f3ddc-82e3-4f63-a9ff-b7a698c6f576">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/655c2d31-b528-46a4-9214-9b0e14954db0">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/32b2add7-a435-46b5-a87e-50e7238871d8">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/06fc4cbe-ea44-49d8-81a1-c3305f875965">
<img width="1100" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/1851e28d-5166-4f97-be8b-99358cccc87e">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/80cafd2c-327a-4117-b4e5-de81f8641b96">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/9b6cf517-03b4-4403-9c7e-c52a28439bc8">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/7e539900-ea17-4c52-8ac0-b4acead8949e">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/00871042-54da-400d-b5f5-07e40c502045">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/119d850a-cf2c-4b85-a93b-bb0f1fcf8202">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/7aa7fd17-1d3f-477d-934e-28acc6df0173">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/9a06c4de-d1c9-4308-914e-a439e8db9bea">
<img width="1110" alt="image" src="https://github.com/Regan17/File_sharing_unfinished/assets/100128424/2aaabe39-cf3a-4c6b-9c24-b82172dd9141">

