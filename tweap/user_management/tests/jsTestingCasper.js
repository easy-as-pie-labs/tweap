var baseUrl = "http://127.0.0.1:8000";
baseUrl = "http://tweap.de";

casper.test.begin('register account', function suite(test) {
    casper.start(baseUrl + "/users/register", function () {
        test.assertTitle("Tweap", "Title is ok");
        test.assertUrlMatch("/register/", "register page was found");
    });

    casper.waitForSelector('#register-form', function () {
        this.fillSelectors('form#register-form', {
            'input[name = username]': 'casperjs',
            'input[name = email]': 'casperjs@gmail.com',
            'input[name = password]': 'test'
        });
    });

    casper.then(function () {
        this.evaluate(function () {
            $('form#register-form').submit();
        });
    });

    casper.waitForUrl(/dashboard\/$/, function () {
        test.assertUrlMatch("/dashboard/", "register and redirect to dashboard successful");
        casper.waitForSelector("#navbar_logout_link").thenClick("#navbar_logout_link");
    });

    casper.then(function () {
        test.assertExists('#navbar_login_link', "logout successful");
    });

    casper.run(function () {
        test.done();
    });
});