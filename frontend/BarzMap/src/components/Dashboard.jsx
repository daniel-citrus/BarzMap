import Header from './Header';
import useUserLogin from '../hooks/useUserLogin';

const Dashboard = () => {
    useUserLogin();

    return (
        <>
            <Header />
        </>
    );
};

export default Dashboard;
