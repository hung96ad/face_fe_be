import * as React from 'react';
import { useState } from 'react';
import Box from '@mui/material/Box';

import {
    useTranslate,
    DashboardMenuItem,
    MenuItemLink,
    MenuProps,
    useSidebarState,
} from 'react-admin';

import users from '../users';
import rooms from '../rooms';

const Menu = ({ dense = false }: MenuProps) => {
    const [state, setState] = useState({
        menuCatalog: true,
        menuSales: true,
        menuCustomers: true,
    });
    const translate = useTranslate();
    const [open] = useSidebarState();

    return (
        <Box
            sx={{
                width: open ? 200 : 50,
                marginTop: 1,
                marginBottom: 1,
                transition: theme =>
                    theme.transitions.create('width', {
                        easing: theme.transitions.easing.sharp,
                        duration: theme.transitions.duration.leavingScreen,
                    }),
            }}
        >
            <DashboardMenuItem />
            <MenuItemLink
                to="/users"
                state={{ _scrollToTop: true }}
                primaryText={translate(`resources.users.name`, {
                    smart_count: 2,
                })}
                leftIcon={<users.icon />}
                dense={dense}
            />
            <MenuItemLink
                to="/rooms"
                state={{ _scrollToTop: true }}
                primaryText={translate(`resources.users.room`, {
                    smart_count: 2,
                })}
                leftIcon={<rooms.icon />}
                dense={dense}
            />
        </Box>
    );
};

export default Menu;