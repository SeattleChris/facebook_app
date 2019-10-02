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

## Adding Influencers to our App

1. Influencer has a Facebook page and an instagram business/creator account.
2. They go to our site and give permission to our app, gives us an auth token
3. Use this auth token, get some basic data of influencer, add to our database.
4. API calls: instagram routes give us info of our influencer - store to DB
   1. Unknown: Are we making this API call with business auth, or influencer token auth?

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
