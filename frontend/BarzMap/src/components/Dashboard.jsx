import Header from './Header';
import useAuthentication from '../hooks/useAuthentication';

const Dashboard = () => {
    const { userToken } = useAuthentication();

    return (
        <>
            <Header />
            {userToken}
        </>
    );
};

export default Dashboard;
