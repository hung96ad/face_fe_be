import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  SelectInput,
  ReferenceInput,
  BooleanInput,
  required
} from 'react-admin';

export const CameraEdit: FC = (props: any) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput source="name" required />
      <TextInput source="rtsp" required />
      <ReferenceInput source="id_room" label="Nhóm cha" reference="rooms">
        <SelectInput optionText="name" required />
      </ReferenceInput>
      <SelectInput source="service_type" choices={[
        { id: 'fast', name: 'fast' },
        { id: 'medium', name: 'medium' },
        { id: 'slow', name: 'slow' },
      ]}
        validate={required()}
      />
      <BooleanInput source="status" />
    </SimpleForm>
  </Edit>
);