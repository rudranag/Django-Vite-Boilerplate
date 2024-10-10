import { lazy } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { frontEndURL } from './lib/constants';


const Todo = lazy(() => import('./pages/Todo'));
const Dashboard = lazy(() => import('./pages/dashboard/Dashboard'));
const OrdersList = lazy(() => import('./pages/Orders'));
const ClippedDrawer = lazy(() => import("@/components/ClippedLayout"))



const router = createBrowserRouter(
    [
        {
            path: "/",
            element: <ClippedDrawer />,
            children: [
                {
                    path: "/todo",
                    element: (
                        <Todo />
                    ),
                },
                {
                    path: "/dashboard",
                    element: (
                        <Dashboard />
                    ),
                },
                {
                    path: "/orders",
                    element: (
                        <OrdersList />
                    ),
                },
                
            ],
            
        },
        
    ],
    {
        basename: frontEndURL,
    }
);

const App = () => {
    return <RouterProvider router={router} />;
};

export default App;
