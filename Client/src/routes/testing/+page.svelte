
<script>
    
	import { onMount } from 'svelte';




    let LastHumanId;
    let LastTransactionId;
    let LastUserId;
    let LastEmail;
    let LastPassword;
    let LastSessionId;
    
    onMount(async () => {
        TESTINGGetLastHuman() ;
        TESTINGGetLastTransaction() ;
        TESTINGGetLastUser() ;
        TESTINGGetLastUserSession();

        
    });

    
    
    function TESTINGGetLastHuman() {
        fetch('http://127.0.0.1:5000/TESTINGGetLastHuman')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            LastHumanId=data['data']['HumanId'];
        })
    }
    function TESTINGGetLastTransaction() {
        fetch('http://127.0.0.1:5000/TESTINGGetLastTransaction')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            LastTransactionId=data['data']['TransactionId'];
        })
    }
    function TESTINGGetLastUser() {
        fetch('http://127.0.0.1:5000/TESTINGGetLastUser')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            LastUserId=data['data']['UserId'];
            LastEmail=data['data']['Email'];
            LastPassword=data['data']['Password'];
        })
    }
    function TESTINGGetLastUserSession() {
        fetch('http://127.0.0.1:5000/TESTINGGetLastUserSession')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            LastSessionId=data['data']['SessionId'];
        })
    }

</script>

<div class="nv-Page-title ">
    <h1>Unit Test Links</h1>
</div>






<ul>
    
    <u><b>Humans</b></u><br>
    LastHumanId: {LastHumanId}<br>
    <li><a  target="testPage" href="http://127.0.0.1:5000/TESTINGGetLastHuman">/TESTINGGetLastHuman</a></li>
    <li><a target="testPage" href="http://127.0.0.1:5000/InsertHuman?FirstName=Jane&MiddleName=E&LastName=Doe&AKAHumanId={LastHumanId}&School=SampleSchool&SemesterYear=2022">/InsertHuman</a></li>
    <li><a target="testPage" href="http://127.0.0.1:5000/UpdateHuman?HumanId={LastHumanId}&FirstName=Jane&MiddleName=E&LastName=Doe&AKAHumanId={LastHumanId}&School=SampleSchool&SemesterYear=2022">/UpdateHuman</a></li>
    <li><a  target="testPage" href="http://127.0.0.1:5000/DeleteHuman?HumanId={LastHumanId}">/DeleteHuman</a></li>
    
    <u><b>Transactions</b></u><br>
    LastTransactionId: {LastTransactionId}<br>
    <li><a  target="testPage" href="http://127.0.0.1:5000/TESTINGGetLastTransaction">/TESTINGGetLastTransaction</a></li>
    <li><a  target="testPage" href="http://127.0.0.1:5000/InsertTransaction?TransactionDate=2022-03-01&FromHumanId=1&ToHumanId=2&TransactionType=Sale&Notes=Example%20Notes&Act=123&Page=456&NotaryHumanId=3&Volume=789&URL=http%3A%2F%2Fexample.com%2Fdocument&TranscriberId=4">/InsertTransaction</a></li>
    <li><a  target="testPage" href="http://127.0.0.1:5000/UpdateTransaction?TransactionId={LastTransactionId}&TransactionDate=2022-03-01&FromHumanId=1&ToHumanId=2&TransactionType=Sale&Notes=Example%20Notes&Act=123&Page=456&NotaryHumanId=3&Volume=789&URL=http%3A%2F%2Fexample.com%2Fdocument&TranscriberId=4">/UpdateTransaction</a></li>
    <li><a  target="testPage" href="http://127.0.0.1:5000/DeleteTransaction?TransactionId={LastTransactionId}">/DeleteTransaction</a></li>

    <u> <b>Account</b></u><br>
    LastUserId: {LastUserId}<br>
    LastEmail: {LastEmail}<br>
    LastPassword: {LastPassword}<br>
    LastSessionId: {LastSessionId}<br>
    <li><a target="testPage" href="http://127.0.0.1:5000/TESTINGGetLastUser">TESTINGGetLastUser</a></li>
    <li><a target="testPage" href="http://127.0.0.1:5000/TESTINGGetLastUserSession">TESTINGGetLastUserSession</a></li>
    <li><a target="testPage" href="http://127.0.0.1:5000/InsertUser?FirstName=John&LastName=Doe&Email=johndoe@example.com&Password=pa$$w0rd">InsertUser</a></li>
    <li><a target="testPage" href="http://127.0.0.1:5000/UpdateUser?UserId=1&FirstName=John&LastName=Doe&Email=johndoe@example.com&Password=pa$$w0rd">UpdateUser</a></li>
    <li><a target="testPage" href="http://127.0.0.1:5000/DeleteUser?UserId=1">DeleteUser</a></li>
    <li><a target="testPage" href="http://127.0.0.1:5000/Login?Email={LastEmail}&Password={LastPassword}">Login</a></li>
    <li><a target="testPage" href="http://127.0.0.1:5000/UpdatePassword?SessionId=1&Password={LastPassword}">UpdatePassword</a></li>
    <li><a target="testPage" href="http://127.0.0.1:5000/VerifyLogin?SessionId={LastSessionId}">VerifyLogin</a></li>
    
</ul>
