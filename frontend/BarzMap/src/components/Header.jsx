import LoginButton from './Login';
import LogoutButton from './Logout';
import { useAuth0 } from '@auth0/auth0-react';

const Header = () => {
    const { isAuthenticated } = useAuth0();
    return <>{isAuthenticated ? <LogoutButton /> : <LoginButton />}</>;
};

export default Header;
