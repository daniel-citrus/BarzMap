import { useAuth0 } from '@auth0/auth0-react';
import { useState, useEffect } from 'react';

const useAuthentication = () => {
    const { user, getAccessTokenSilently } = useAuth0();
    const [userToken, setUserToken] = useState();

    useEffect(() => {
        async function fetchData() {
            try {
                const accessToken = await getAccessTokenSilently();
                setUserToken(accessToken);
            } catch (e) {
                console.error('useAuthentication Error: ', e);
            }
        }

        fetchData();
    }, [user, getAccessTokenSilently]);

    return { userToken };
};

export default useAuthentication;
