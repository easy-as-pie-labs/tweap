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
        casper.waitForSelector("#project_dropdown").thenClick("#project_dropdown");
        casper.waitForSelector("#navbar_new_link").thenClick("#navbar_new_link");
    });

    casper.waitForUrl(/projects\/new\/$/, function() {
        test.assertUrlMatch("/projects/new/", "new project button was found, redirected to create project page");
        //casper.waitForSelector("#navbar_logout_link").thenClick("#navbar_logout_link");
    });

    casper.waitForSelector('#new_project_form', function () {
        this.fillSelectors('form#new_project_form', {
            'input[name = name]': 'casper\'s project'
        });
    });

    casper.then(function () {
//        this.evaluate(function () {
//            $('form#new_project_form').submit();
//        });
        casper.waitForSelector('.btn').thenClick('.btn');
    });

    casper.waitForSelector('#project_title_header', function() {
        test.assertEvalEquals(function () {
            return __utils__.findOne('#project_title_header').textContent;
        }, ' casper\'s project', "project was created with name");
        test.assertElementCount("li.project_dropdown_li", 1, "one project exists for user");
        casper.waitForSelector("#navbar_logout_link").thenClick("#navbar_logout_link");
    });

    casper.run(function () {
        test.done();
    });
});

// TODO: accept project invitation
casper.test.begin('accept project invitation', function suite(test) {
    casper.start(baseUrl + "/users/register", function () {
        test.assertTitle("Tweap", "Title is ok");
        test.assertUrlMatch("/register/", "register page was found");
    });

    casper.waitForSelector('#register-form', function () {
        this.fillSelectors('form#register-form', {
            'input[name = username]': 'anothercasper',
            'input[name = email]': 'anothercasper@gmail.com',
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
        casper.waitForSelector("#project_dropdown").thenClick("#project_dropdown");
        casper.waitForSelector("#navbar_new_link").thenClick("#navbar_new_link");
    });

    casper.waitForUrl(/projects\/new\/$/, function() {
        test.assertUrlMatch("/projects/new/", "new project button was found, redirected to create project page");
    });

    casper.waitForSelector('#new_project_form', function () {
        this.fillSelectors('form#new_project_form', {
            'input[name = name]': 'anothercasper\'s project',
            'input[name = userinput]': 'casperjs'
        });

        casper.waitForSelector('.addUserButton').thenClick('.addUserButton');
    });

    casper.then(function () {
//        this.evaluate(function () {
//            $('form#new_project_form').submit();
//        });
        casper.waitForSelector('.btn').thenClick('.btn');
    });

    casper.waitForSelector(".accepted_user_label", function() {
        test.assertEvalEquals(function () {
            return __utils__.findOne('#project_title_header').textContent;
        }, ' anothercasper\'s project', "project was created with name");
        test.assertElementCount("li.project_dropdown_li", 1, "one project exists for user");
        test.assertElementCount("span.accepted_user_label", 1, "one user was added");
        test.assertElementCount("span.invited_user_label", 1, "one user was invited");
        casper.waitForSelector("#navbar_logout_link").thenClick("#navbar_logout_link");
    });

    casper.then(function() {
        casper.waitForSelector("#navbar_login_link").thenClick("#navbar_login_link");
    });

    casper.waitForSelector("#login-form", function () {
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
        test.assertElementCount("strong.invitation_title", 1, "user has one invitation");
        casper.waitForSelector('.acceptInvitation').thenClick('.acceptInvitation');
    });

    casper.waitForSelector(".accepted_user_label", function () {
        test.assertEvalEquals(function () {
            return __utils__.findOne('#project_title_header').textContent;
        }, ' anothercasper\'s project', "was redirected to project after acceepting invitation");
        test.assertElementCount("li.project_dropdown_li", 2, "two projects exists for user");
        test.assertElementCount("span.accepted_user_label", 2, "two users are now in project");
        test.assertElementCount("span.invited_user_label", 0, "0 pending invitations");
        casper.waitForSelector("#navbar_logout_link").thenClick("#navbar_logout_link");
    });

    casper.run(function () {
        test.done();
    });
});

// TODO: reject project invitation
casper.test.begin('reject project invitation', function suite(test) {
    casper.start(baseUrl + "/users/login", function () {
        test.assertTitle("Tweap", "Title is ok");
        test.assertUrlMatch("/login/", "login page was found");
    });

    casper.waitForSelector('#login-form', function () {
        this.fillSelectors('form#login-form', {
            'input[name = username]': 'anothercasper',
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
        casper.waitForSelector("#project_dropdown").thenClick("#project_dropdown");
        casper.waitForSelector("#navbar_new_link").thenClick("#navbar_new_link");
    });

    casper.waitForUrl(/projects\/new\/$/, function() {
        test.assertUrlMatch("/projects/new/", "new project button was found, redirected to create project page");
    });

    casper.waitForSelector('#new_project_form', function () {
        this.fillSelectors('form#new_project_form', {
            'input[name = name]': 'yetanothercasper\'s project',
            'input[name = userinput]': 'casperjs'
        });
        casper.waitForSelector('.addUserButton').thenClick('.addUserButton');
    });

    casper.then(function () {
//        this.evaluate(function () {
//            $('form#new_project_form').submit();
//        });
        casper.waitForSelector('.btn').thenClick('.btn');
    });

    casper.waitForSelector(".accepted_user_label", function () {
        test.assertEvalEquals(function () {
            return __utils__.findOne('#project_title_header').textContent;
        }, ' yetanothercasper\'s project', "project was created with name");
        test.assertElementCount("li.project_dropdown_li", 2, "two projects exists for user");
        test.assertElementCount("span.accepted_user_label", 1, "one user was added");
        test.assertElementCount("span.invited_user_label", 1, "one user was invited");
        casper.waitForSelector("#navbar_logout_link").thenClick("#navbar_logout_link");
        casper.waitForSelector("#navbar_login_link").thenClick("#navbar_login_link");
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
        test.assertElementCount("strong.invitation_title", 1, "user has one invitation");
        test.assertElementCount("li.project_dropdown_li", 2, "two projects exists for user");
        casper.waitForSelector('.rejectInvitation').thenClick('.rejectInvitation');
    });

    casper.waitForUrl(/dashboard\/$/, function () {
        test.assertUrlMatch("/dashboard/", "rejected invitation, no redirect");
        test.assertElementCount("li.project_dropdown_li", 2, "still two projects exists for user");
        casper.waitForSelector("#navbar_logout_link").thenClick("#navbar_logout_link");
    });

    casper.run(function () {
        test.done();
    });
});

// TODO: edit project
casper.test.begin('edit project', function suite(test) {
    casper.start(baseUrl + "/users/login", function () {
        test.assertTitle("Tweap", "Title is ok");
        test.assertUrlMatch("/login/", "login page was found");
    });

    casper.waitForSelector('#login-form', function () {
        this.fillSelectors('form#login-form', {
            'input[name = username]': 'anothercasper',
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
        casper.waitForSelector(".project_dropdown_a").thenClick(".project_dropdown_a");
    });

    casper.waitForUrl(/projects/, function() {
        test.assertUrlMatch("/projects/", "login and redirect to dashboard successful");
        casper.waitForSelector("#edit_project_button").thenClick("#edit_project_button");
    });

    casper.waitForUrl(/projects\/edit/, function() {
        test.assertUrlMatch("/projects/edit/", "redirected to project edit view");
        casper.waitForSelector('#new_project_form', function () {
            this.fillSelectors('form#new_project_form', {
                'input[name = name]': 'edited project'
            });
        });

        casper.then(function () {
//            this.evaluate(function () {
//                $('form#new_project_form').submit();
//            });
            casper.waitForSelector('.btn').thenClick('.btn');
        });
    });

    casper.waitForUrl(/projects/, function() {
        test.assertUrlMatch("/projects/", "redirected to project view");
        casper.waitForSelector(".accepted_user_label", function() {
            test.assertEvalEquals(function () {
                return __utils__.findOne('#project_title_header').textContent;
            }, ' edited project', "project name was edited");
        });
        test.assertElementCount("li.project_dropdown_li", 2, "still two projects exists for user");
        casper.waitForSelector("#leave_project_button").thenClick("#leave_project_button");
        casper.waitForSelector("#leave_project_confirm_button").thenClick("#leave_project_confirm_button");
    });

    casper.waitForUrl(/dashboard\/$/, function() {
        test.assertUrlMatch("/dashboard/", "redirected to dashboard");
        test.assertElementCount("li.project_dropdown_li", 1, "now the user only has one project left");
    });

    casper.then(function () {
        casper.waitForSelector("#navbar_profile_link").thenClick("#navbar_profile_link");
    });

    casper.waitForUrl(/profile\/anothercasper\/$/, function () {
        test.assertUrlMatch("/profile/anothercasper/", "profile page was found");
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

    casper.then(function () {
        casper.waitForSelector("#navbar_login_link").thenClick("#navbar_login_link");
    });

    casper.waitForUrl(/users\/login\/$/, function () {
        test.assertUrlMatch("/login/", "login page was found");
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

// TODO: leave project
casper.test.begin('leave project', function suite(test) {
    test.done();
});
