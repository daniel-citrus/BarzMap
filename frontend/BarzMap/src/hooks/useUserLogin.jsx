import useAuthentication from '../hooks/useAuthentication';
import { useAuth0 } from '@auth0/auth0-react';
import { useEffect } from 'react';

const useUserLogin = () => {
    const { userToken } = useAuthentication();
    const { isAuthenticated, user } = useAuth0();

    useEffect(() => {
        async function loginUser() {
            if (isAuthenticated && userToken) {
                try {
                    let response = await fetch(
                        `${import.meta.env.VITE_BACKEND_API}/auth/validate`,
                        {
                            method: 'POST',
                            headers: {
                                Authorization: `Bearer ${userToken}`,
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                userToken,
                                firstName: user.given_name,
                                lastName: user.family_name,
                                profile_picture_url: user.picture,
                                email: user.email,
                            }),
                        }
                    );

                    response = await response.json();
                    console.log(response);
                } catch (e) {
                    console.error('Login Issue: ', e);
                }
            }
        }

        loginUser();
    }, [isAuthenticated, userToken, user]);
};

export default useUserLogin;
