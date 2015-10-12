
var baseUrl = "http://127.0.0.1:8000";
//var baseUrl = "http://dev.tweap.easy-as-pie.de";

casper.test.begin('create project', function suite(test) {
    casper.start(baseUrl + "/users/register", function () {
        test.assertUrlMatch("/register/", "register page was found");
        test.assertTitle("Tweap", "Title is ok");
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
    });
});
