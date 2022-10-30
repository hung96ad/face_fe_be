import React, { FC } from 'react';
import {
  Create,
  SimpleForm,
  TextInput,
  SelectInput,
  ReferenceInput,
  required
} from 'react-admin';

export const CameraCreate: FC = (props: any) => (
  <Create {...props} title={"Tạo mới nhóm phòng"}>
    <SimpleForm defaultValues={{
      status: true,
    }}>
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
    </SimpleForm>
  </Create>
);
