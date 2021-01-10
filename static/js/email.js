function sendMail(contactForm) {
    emailjs
        .send("gmail", "comics", {
            from_name: contactForm.name.value,
            from_email: contactForm.email.value,
            contact_body: contactForm.message.value,
        })
        .then(
            //When email sends.
            function(response) {
                console.log("SUCCESS", response);
                let load = document.getElementById("submitbutton").innerHTML;
                let done = load.replace("Submit", "Sent!");
                document.getElementById("submitbutton").innerHTML = done;
                document.getElementById("submitbutton").disabled = true;
                document.getElementById("contact").reset();
            },
            //If email doesn't send.
            function(error) {
                console.log("FAILED", error);
                let load = document.getElementById("submitbutton").innerHTML;
                let fail = load.replace("Submit", "Try Again Later");
                document.getElementById("submitbutton").innerHTML = fail;
            }
        );

    //Avoid reloading page after email has been sent.
    return false;
}