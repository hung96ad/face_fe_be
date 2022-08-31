import { Card, CardContent } from "@mui/material";
import { FilterList, FilterListItem, useGetList } from 'react-admin';
import { useEffect, useState } from "react";

function list_to_tree(list: any[]) {
    var map: { [index: string]: any } = {}, node, roots = [], i;
    for (i = 0; i < list.length; i += 1) {
        map[list[i].id] = i; // initialize the map
        list[i].children = []; // initialize the children
    }

    for (i = 0; i < list.length; i += 1) {
        node = list[i];
        if (node.parent_id) {
            list[map[node.parent_id]].children.push(node);
        } else {
            roots.push(node);
        }
    }
    return roots;
}

const Aside = () => {
    const [state, setState] = useState<any[]>([]);
    // const [parentId, setParentId] = useState(null);
    const { data, isLoading } = useGetList(
        'rooms',
        {
            pagination: { page: 1, perPage: 100000 },
            // filter: { parent_id: parentId }
        }
    );
    useEffect(() => {
        if (data) {
            const arrToTreeRes = list_to_tree(data);
            console.log(arrToTreeRes);
            setState(oldArray => [...oldArray, ...arrToTreeRes]);
        }
    }, [isLoading]);

    const listFilters = state.map((f, key) => {
        return (<FilterListItem
            key={key}
            label={f.name}
            value={{ id_room: f.id }}
        />)
    });

    return (
        <Card sx={{
            display: {
                xs: 'none',
                md: 'block',
            },
            order: -1,
            flex: '0 0 15em',
            mr: 2,
            mt: 8,
            alignSelf: 'flex-start',
        }}>
            <CardContent sx={{ pt: 1 }}>
                <FilterList label="filter.room"
                    icon={null}>
                    <FilterList
                        label={"1"}
                        icon={null}
                    >
                        {listFilters}
                    </FilterList>

                </FilterList>
            </CardContent>
        </Card>
    )
}
export default Aside;
