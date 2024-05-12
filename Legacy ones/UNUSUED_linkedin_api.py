from linkedin import linkedin

APPLICATON_KEY    = '78h8iawd1r9jby'
APPLICATON_SECRET = 'WPL_AP0.CZIf9l8NtmOpml7n.NTA1MDk2ODY0'

RETURN_URL = 'http://localhost:8080'

authentication = linkedin.LinkedInAuthentication(
                    APPLICATON_KEY,
                    APPLICATON_SECRET,
                    RETURN_URL,
                    linkedin.PERMISSIONS.enums.values()
                )

# Optionally one can send custom "state" value that will be returned from OAuth server
# It can be used to track your user state or something else (it's up to you)
# Be aware that this value is sent to OAuth server AS IS - make sure to encode or hash it
#authorization.state = 'your_encoded_message'

print(authentication.authorization_url)  # open this url on your browser

# https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=78h8iawd1r9jby&scope=r_basicprofile%20r_emailaddress%20w_share%20rw_company_admin%20r_fullprofile%20r_contactinfo&state=6df52709bb47fa6681faf92065d5add0&redirect_uri=http%3A//localhost%3A8000
#
# https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=78h8iawd1r9jby&scope=r_basicprofile%20r_emailaddress%20w_share%20rw_company_admin%20r_fullprofile%20r_contactinfo&state=6df52709bb47fa6681faf92065d5add0&redirect_uri=http%3A//localhost%3A8000
