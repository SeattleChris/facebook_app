# Research on Tools & Techniques used

Use the Facebook Login product to request User access tokens from your app's users. Note that Page tokens are not supported. Instagram users must connect their Instagram Business Account or Instagram Creator Account to a Facebook Page before your app can access the API on their behalf. Once connected, any Facebook User who is able to perform Tasks on that Page can grant your app an access token, which can then be used in API requests.
- https://developers.facebook.com/docs/instagram-api/overview

            FB.getLoginStatus(function(response) {
              if (response.status === 'connected') {
                let accessToken = response.authResponse.accessToken;
                if (accessToken) {
                  console.log('Got Access Token');
                }
              }
            });
  Response:
            {
                status: 'connected',
                authResponse: {
                    accessToken: '{access-token}',
                    expiresIn:'{unix-timestamp}',
                    reauthorize_required_in:'{seconds-until-token-expires}',
                    signedRequest:'{signed-parameter}',
                    userID:'{user-id}'
                }
            }

## Adding Influencers to our App

1. Influencer has a Facebook page and an instagram business/creator account.
2. They go to our site and give permission to our app, gives us an auth token
   1. The Facebook SDK for Javascript obtains and persists user access tokens automatically in browser cookies. You can retrieve the user access token by making a call to FB.getAuthResponse which will include an accessToken property within the response. See code block below.
   2. A request for oauth has optional parameters, with `code` being the default for `response_type`.


3. . Use this auth token, get some basic data of influencer, add to our database.
4. API calls: instagram routes give us info of our influencer - store to DB
   1. Unknown: Are we making this API call with business auth, or influencer token auth?
5. [FaceBook Longer Example](https://developers.facebook.com/docs/facebook-login/web#logindialog)

Example 1:
```js
  FB.getLoginStatus(function(response) {
    if (response.status === 'connected') {
      var accessToken = response.authResponse.accessToken;
    }
  } );
```

See also "Manual Build a Login"

### Manual Build A Login - Adding a New User

Your app must initiate a redirect to an endpoint which will display the login dialog.

1. [x] We have our app-token, which is never passed by front-end. Our app-id can be passed front-end.
2. [x] New User can login w/ FB passed along with our app-id. They grant permissions we request.
3. [x] Capture the returning user auth-token.
4. [ ] Capture facebook user_id to validate against in backend.
5. [ ] Backend takes user token, and verifies w/ our app token.
6. [ ] Take the response and verify is_valid is true, and user_id matches as expected.
7. [ ] Add user to our DB, populating with info from FB account.

Request from us:
```
https://www.facebook.com/v4.0/dialog/oauth?
  client_id={app-id}
  &redirect_uri={redirect-uri}
  &state={state-param}
```

Response:
```
https://www.domain.com/login?state="{state-param}"
```

With optional parameters, with `code` as default for  `response_type`.

To get an access token, after getting `code`, we need to make a server-to-server request
```
GET https://graph.facebook.com/v4.0/oauth/access_token?
   client_id={app-id}
   &redirect_uri={redirect-uri}
   &client_secret={app-secret}
   &code={code-parameter}
```

Expected response:
```
{
  "access_token": {access-token},
  "token_type": {type},
  "expires_in":  {seconds-til-expiration}
}
```

We then check the access token:
```
GET graph.facebook.com/debug_token?
     input_token={token-to-inspect}
     &access_token={app-token-or-admin-token}
```

Expected response:
```
{
    "data": {
        "app_id": 138483919580948,
        "type": "USER",
        "application": "Social Cafe",
        "expires_at": 1352419328,
        "is_valid": true,
        "issued_at": 1347235328,
        "metadata": {
            "sso": "iphone-safari"
        },
        "scopes": [
            "email",
            "publish_actions"
        ],
        "user_id": "1207059"
    }
}
```
We use the `app_id` and `user_id` to verify the access token is valid for this user.

## Influencer connecting Instagram to a FaceBook Page

1. Influencer must have an influencer instagram account (or fix it following steps).
2. Influencer must have a FaceBook Page (Business Page).
3. On their FaceBook Page, click settings, then instagram, then attach instagram account.
4. While here: Make sure their instagram is an influencer account (switch to business profile).

## Needed for Development Testing

During development, we can only access content connected to people who have roles in the FaceBook app (with FaceBook Developer account), and test accounts. See [Test User API](https://developers.facebook.com/docs/graph-api/reference/v4.0/test-user)

- Test Users
- Test Pages (owned by Test users)

## Needed for FaceBook App approval

1. Update Privacy Policy: [Privacy Policy](https://fb-test-251219.appspot.com/privacy)
2. [App Review](https://developers.facebook.com/docs/apps/review)
