class Account 
{
    constructor() {}
    constructor(username, password, account_id, email, fullName, isDeveloper)
    {
        this.username = username;
        this.password = password;
        this.account_id = account_id;
        this.email = email;
        this.fullName = fullName;
        this.isDeveloper = isDeveloper;
    }

    login()
    {
        usernInput = document.getElementById('username').value;
        pwordInput = document.getElementById('InputPassword1').value;
        this.veririfiedLogin(usernInput, pwordInput);
        
    };

    register(){};
    updateProfile(){};
    veririfiedLogin(usernInput, pwordInput)
    {

    };
}