function test(name) {
    console.log("Hi " + name);
}

// This will invoke ajax request to server to login the user
function checkLogin() {

    // validate input

    $.ajax({
        url: "/login",
        data: $("#loginForm").serialize(),
        type: "POST",
        datatype: "json", 
        success: function(response){
            console.log(response);

            if (response.status == true) {
                // Redirect to profile 
                window.location.href = response.data;
            } else {
                // 0 means "not found"
                $("#statusDiv").text(response.error);
                $("#statusDiv").show();
            }
        }, 
        error: function(error){
            console.log(error);
        }
    });

}


// {
//             "userName": email,
//             "password": password
//         },



function saveComment() {

    // validate input

    $.ajax({
        url: "/save_comment",
        data: $("#saveCommentForm").serialize(),
        type: "POST",
        datatype: "json", 
        success: function(response){
            console.log(response);

            // $("#commentsTable tbody").append("<tr><td>" + response.data.user_name + "</td><td>&nbsp;</td><td>" + response.data.comment + "</br></td></tr>");
            // $("#commentsDiv").append(response.data.user_name + ' ' + response.data.comment);

            // if (response.status == true) {
            //     // Redirect to profile 
            //     window.location.href = response.data;
            // } else {
            //     // 0 means "not found"
            //     $("#statusDiv").text(response.error);
            //     $("#statusDiv").show();
            // }
        }, 
        error: function(error){
            console.log(error);
        }
    });

}
