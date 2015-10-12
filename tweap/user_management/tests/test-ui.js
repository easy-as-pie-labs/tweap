var baseUrl = "http://127.0.0.1:8000";
var baseUrl = "http://tweap.de";

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

casper.test.begin('login', function suite(test) {
    casper.start(baseUrl + "/users/login", function () {
        test.assertTitle("Tweap", "Title is ok");
        test.assertUrlMatch("/login/", "login page was found");
    });

    casper.waitForSelector('#login-form', function () {
        this.fillSelectors('form#login-form', {
            'input[name = username]': 'casperjs',
            'input[name = password]': 'test'
        });
    });

    casper.then(function () {
        this.evaluate(function () {
            $('form#login-form').submit();
        });
    });

    casper.waitForUrl(/dashboard\/$/, function () {
        test.assertUrlMatch("/dashboard/", "login and redirect to dashboard successful");
        casper.waitForSelector("#navbar_logout_link").thenClick("#navbar_logout_link");
    });

    casper.waitForSelector('#navbar_login_link', function () {
        test.assertExists('#navbar_login_link', "logout successful");
    });

    casper.run(function () {
        test.done();
    });
});

casper.test.begin('delete account', function suite(test) {
    casper.start(baseUrl + "/users/login", function () {
        test.assertTitle("Tweap", "Title is ok");
        test.assertUrlMatch("/login/", "login page was found");
    });

    casper.waitForSelector('#login-form', function () {
        this.fillSelectors('form#login-form', {
            'input[name = username]': 'casperjs',
            'input[name = password]': 'test'
        });
    });

    casper.then(function () {
        this.evaluate(function () {
            $('form#login-form').submit();
        });
    });

    casper.waitForUrl(/dashboard\/$/, function () {
        test.assertUrlMatch("/dashboard/", "login and redirect to dashboard successful");
        casper.waitForSelector("#navbar_profile_link").thenClick("#navbar_profile_link");
    });

    casper.waitForUrl(/profile\/casperjs\/$/, function () {
        test.assertUrlMatch("/profile/casperjs/", "profile page was found");
        casper.waitForSelector("#make_changes").thenClick("#make_changes");
    });

    casper.waitForUrl(/editprofile/, function () {
        test.assertUrlMatch("/editprofile/", "edit profile page was found");
        casper.waitForSelector("#delete_account").thenClick("#delete_account");
    });

    casper.waitForUrl(/delete\/$/, function () {
        test.assertUrlMatch("/delete/", "delete profile page was found");
        casper.waitForSelector("#confirm").thenClick("#confirm");
        casper.waitForSelector("#delete_account").thenClick("#delete_account");
    });

    casper.waitForUrl(/dashboard\/$/, function () {
        test.assertUrlMatch("/dashboard/", "delete account and redirect to dashboard successful");
    });

    casper.run(function () {
        test.done();
    });
});

casper.test.begin('edit profile', function suite(test) {
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
        casper.waitForSelector("#navbar_profile_link").thenClick("#navbar_profile_link");
    });

    casper.waitForUrl(/profile\/casperjs\/$/, function () {
        test.assertUrlMatch("/profile/casperjs/", "profile page was found");
        casper.waitForSelector("#make_changes").thenClick("#make_changes");
    });

    casper.waitForUrl(/editprofile/, function () {
        test.assertUrlMatch("/editprofile/", "edit profile page was found");

        casper.waitForSelector('#edit_profile_form', function () {
            this.fillSelectors('form#edit_profile_form', {
                'input[name = first_name]': 'Casper',
                'input[name = last_name]': 'JS'
            });
        });

        casper.then(function () {
            this.evaluate(function () {
                $('form#edit_profile_form').submit();
            });
        });
    });

    casper.waitForUrl(/profile\/casperjs\/$/, function () {
        test.assertUrlMatch("/profile/casperjs/", "profile was updated and redirected to profile view");
        test.assertEvalEquals(function () {
            return __utils__.findOne('#profile_name').textContent;
        }, 'Casper JS', "first name and last name was updated");
    });

    casper.then(function () {
        casper.waitForSelector("#make_changes").thenClick("#make_changes");
    });

    casper.waitForUrl(/editprofile/, function () {
        test.assertUrlMatch("/editprofile/", "edit profile page was found");

        casper.waitForSelector('#edit_profile_form', function(){
            this.fillSelectors('form#edit_profile_form', {
                'input[name = first_name]': 'Casper',
                'input[name = last_name]': ''
            });
        });

        casper.then(function () {
            this.evaluate(function () {
                $('form#edit_profile_form').submit();
            });
        });
    });

    casper.waitForUrl(/profile\/casperjs\/$/, function () {
        test.assertUrlMatch("/profile/casperjs/", "profile was updated and redirected to profile view");
        test.assertEvalEquals(function () {
            return __utils__.findOne('#profile_name').textContent;
        }, 'Casper', "only first name was updated");
    });

    casper.then(function () {
        casper.waitForSelector("#make_changes").thenClick("#make_changes");
    });

    casper.waitForUrl(/editprofile/, function () {
        test.assertUrlMatch("/editprofile/", "edit profile page was found");
        casper.waitForSelector('#edit_profile_form', function () {
            this.fillSelectors('form#edit_profile_form', {
                'input[name = first_name]': '',
                'input[name = last_name]': 'JS'
            });
        });

        casper.then(function () {
            this.evaluate(function () {
                $('form#edit_profile_form').submit();
            });
        });
    });

    casper.waitForUrl(/profile\/casperjs\/$/, function () {
        test.assertUrlMatch("/profile/casperjs/", "profile was updated and redirected to profile view");
        test.assertEvalEquals(function () {
            return __utils__.findOne('#profile_name').textContent;
        }, 'JS', "only last name was updated");
    });

    casper.then(function () {
        test.assertUrlMatch("/profile/casperjs/", "profile page was found");
        casper.waitForSelector("#make_changes").thenClick("#make_changes");
    });

    casper.waitForUrl(/editprofile/, function () {
        test.assertUrlMatch("/editprofile/", "edit profile page was found");
        casper.waitForSelector("#delete_account").thenClick("#delete_account");
    });

    casper.waitForUrl(/delete\/$/, function () {
        test.assertUrlMatch("/delete/", "delete profile page was found");
        casper.waitForSelector("#confirm").thenClick("#confirm");
        casper.waitForSelector("#delete_account").thenClick("#delete_account");
    });

    casper.waitForUrl(/dashboard\/$/, function () {
        test.assertUrlMatch("/dashboard/", "delete account and redirect to dashboard successful");
    });

    casper.run(function () {
        test.done();
    });
});
