import { Button } from '@mui/material';
import ContentAdd from '@mui/icons-material/Add';
import { Link } from 'react-router-dom';

const CreateRoomButton = (record: any) => {
    return (
        <Button
            component={Link}
            to={{
                pathname: '/rooms/create',
            }}
            state={{ record: { parent_id: record.record.id } }}
            size={'small'}
        >
            <ContentAdd /> Create
        </Button>
    )
};
export default CreateRoomButton;