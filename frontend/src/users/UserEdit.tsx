import * as React from 'react';
import {
    Edit,
    TextInput,
    PasswordInput,
    SimpleForm,
    useTranslate,
    BooleanInput,
} from 'react-admin';
import { Grid, Box, Typography } from '@mui/material';

import { validateForm } from './UserCreate';

const UserEdit = () => {
    const translate = useTranslate();
    return (
        <Edit>
            <SimpleForm validate={validateForm}>
                <Grid container width={{ xs: '100%', xl: 800 }} spacing={2}>
                    <Grid item xs={12} md={8}>
                        <Typography variant="h6" gutterBottom>
                            {translate(
                                'resources.customers.fieldGroups.identity'
                            )}
                        </Typography>
                        <Box display={{ xs: 'block', sm: 'flex' }}>
                            <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                <TextInput
                                    source="first_name"
                                    isRequired
                                    fullWidth
                                />
                            </Box>
                            <Box flex={1} ml={{ xs: 0, sm: '0.5em' }}>
                                <TextInput
                                    source="last_name"
                                    isRequired
                                    fullWidth
                                />
                            </Box>
                        </Box>
                        <TextInput
                            type="email"
                            source="email"
                            isRequired
                            fullWidth
                        />
                        <BooleanInput source="is_superuser" />
                        <BooleanInput source="is_active" />

                        <Box mt="1em" />

                        <Typography variant="h6" gutterBottom>
                            {translate(
                                'resources.customers.fieldGroups.address'
                            )}
                        </Typography>
                        <TextInput
                            source="address"
                            multiline
                            fullWidth
                            helperText={false}
                        />

                        <Box mt="1em" />

                        <Typography variant="h6" gutterBottom>
                            {translate(
                                'resources.customers.fieldGroups.change_password'
                            )}
                        </Typography>
                        <Box display={{ xs: 'block', sm: 'flex' }}>
                            <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                <PasswordInput
                                    source="password"
                                    fullWidth
                                />
                            </Box>
                            <Box flex={1} ml={{ xs: 0, sm: '0.5em' }}>
                                <PasswordInput
                                    source="confirm_password"
                                    fullWidth
                                />
                            </Box>
                        </Box>
                    </Grid>
                </Grid>
            </SimpleForm>
        </Edit>
    );
};

export default UserEdit;