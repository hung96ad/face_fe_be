import * as React from 'react';
import { useCallback } from 'react';
import { List } from 'react-admin';
import { matchPath, useLocation, useNavigate } from 'react-router-dom';
import { Box, Drawer} from '@mui/material';
import userFilters from './userFilters';
import UserListDesktop from './UserListDesktop';

const UserList = () => {
    const location = useLocation();
    const navigate = useNavigate();

    const handleClose = useCallback(() => {
        navigate('/users');
    }, [navigate]);

    const match = matchPath('/users/:id', location.pathname);

    return (
        <Box display="flex">
            <List
                sx={{
                    flexGrow: 1,
                    transition: (theme: any) =>
                        theme.transitions.create(['all'], {
                            duration: theme.transitions.duration.enteringScreen,
                        }),
                    marginRight: !!match ? '400px' : 0,
                }}
                filters={userFilters}
                sort={{ field: 'id', order: 'ASC' }}
            >
                <UserListDesktop
                    selectedRow={
                        !!match
                            ? parseInt((match as any).params.id, 10)
                            : undefined
                    }
                />
            </List>
            <Drawer
                variant="persistent"
                open={!!match}
                anchor="right"
                onClose={handleClose}
                sx={{ zIndex: 100 }}
            >
                {/* {!!match && (
                    <ReviewEdit
                        id={(match as any).params.id}
                        onCancel={handleClose}
                    />
                )} */}
            </Drawer>
        </Box>
    );
};

export default UserList;
