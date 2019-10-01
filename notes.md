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
