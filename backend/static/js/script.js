document.querySelectorAll("form").forEach(form => {

    form.addEventListener("submit", function () {

        const button = form.querySelector("button");

        if (button) {

            button.innerHTML = "Please Wait...";
            button.disabled = true;

        }

    });

});