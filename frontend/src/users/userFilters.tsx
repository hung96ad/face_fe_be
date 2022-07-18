import * as React from 'react';
import {
    AutocompleteInput,
    DateInput,
    ReferenceInput,
    SearchInput,
    SelectInput,
} from 'react-admin';
import { User } from '../types';

const userFilters = [
    <SearchInput source="q" alwaysOn />,
    <SelectInput
        source="is_active"
        choices={[
            { id: true, name: 'Accepted' },
            { id: false, name: 'Pending' },
        ]}
    />,
    <SelectInput
        source="is_superuser"
        choices={[
            { id: true, name: 'Admin' },
            { id: false, name: 'User' },
        ]}
    />
];

export default userFilters;
