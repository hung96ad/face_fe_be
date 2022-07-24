import * as React from 'react';
import {
    Identifier,
    Datagrid,
    TextField,
    EmailField,
    BooleanField,
} from 'react-admin';
import rowStyle from './rowStyle';


export interface UserListDesktopProps {
    selectedRow?: Identifier;
}
const UserListDesktop = ({ selectedRow }: UserListDesktopProps) => (
    <Datagrid
        rowClick="edit"
        rowStyle={rowStyle(selectedRow)}
        optimized
        sx={{
            '& .RaDatagrid-thead': {
                borderLeftColor: 'transparent',
                borderLeftWidth: 5,
                borderLeftStyle: 'solid',
            },
            '& .column-comment': {
                maxWidth: '18em',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
            },
        }}
    >
        <TextField source="id" />
        <EmailField source="email" />
        <TextField source="first_name" />
        <TextField source="last_name" />
        <BooleanField source="is_active" />
        <BooleanField source="is_superuser" />
    </Datagrid>
);

export default UserListDesktop;
