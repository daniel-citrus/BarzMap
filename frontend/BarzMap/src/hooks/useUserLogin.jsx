import useAuthentication from '../hooks/useAuthentication';
import { useAuth0 } from '@auth0/auth0-react';
import { useEffect } from 'react';

const useUserLogin = () => {
    const { userToken } = useAuthentication();
    const { isAuthenticated } = useAuth0();

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
                            body: JSON.stringify(),
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
    }, [isAuthenticated, userToken]);

    return <></>;
};

export default useUserLogin;
