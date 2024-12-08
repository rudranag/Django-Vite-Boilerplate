import { lazy, Suspense } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { frontEndURL } from './lib/constants';
import LoadingLayout from './pages/Auth/LoadingLayout';
import { SnackbarProvider } from './context/SnackbarContext';

const Todo = lazy(() => import('./pages/Todo'));
const Dashboard = lazy(() => import('./pages/dashboard/Dashboard'));
const OrdersList = lazy(() => import('./pages/Orders'));
const Login = lazy(() => import('./pages/Auth/Login'));
const Signup = lazy(() => import('./pages/Auth/Signup'));
const ClippedDrawer = lazy(() => import("@/components/ClippedLayout"));

const router = createBrowserRouter(
    [
        {
            path: "/",
            element: (
                <Suspense fallback={<LoadingLayout />}>
                    <ClippedDrawer />
                </Suspense>
            ),
            children: [
                {
                    path: "/todo",
                    element: <Todo />,
                },
                {
                    path: "/dashboard",
                    element: <Dashboard />,
                },
                {
                    path: "/orders",
                    element: <OrdersList />,
                },
            ],
        },
        {
            path: "/login",
            element: (
                <Suspense fallback={<LoadingLayout />}>
                    <SnackbarProvider>
                        <Login />
                    </SnackbarProvider>
                </Suspense>
            ),
        },
        {
            path: "/signup",
            element: (
                <Suspense fallback={<LoadingLayout />}>
                    <SnackbarProvider>
                        <Signup />
                    </SnackbarProvider>
                </Suspense>
            ),
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
