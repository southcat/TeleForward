'use client'

import {Button, Select, Space, Table} from "antd";
import {useEffect, useState} from "react";
import axios from "axios";
import { get } from "@/utils/requests";

export default function Group() {
    const [option, setOption] = useState([]);
    const [selectValue, setSelectValue] = useState("");
    const [groupList, setGroupList] = useState([]);
    const [defaultSelectValue, setDefaultSelectValue] = useState({});//默认选中的值
    const request = async()=>{
        const accountsRes = await get('http://127.0.0.1:8000/account/get-account-pool')
        console.log(accountsRes.data);
        const options = await accountsRes.data.account_pool.map((item) => ({
            value: item.phone_number.toString(),
            title: item.phone_number.toString(),
            label: item.phone_number.toString(),
        }));
        setOption(options);
        setSelectValue(options[0].value);
    }
    const syncGroupList = async()=>{
        const res = await get('http://127.0.0.1:8000/account/insertGroup?phone_number=+'+selectValue)
        getGroupList()

    }
    const getGroupList = async()=>{
        console.log(option)
        const res = await get('http://127.0.0.1:8000/account/get-group-phone?phone_number=+'+selectValue)
        console.log(res.data);
        const groupsWithKey = res.data.groups.map(group => ({
            ...group,
            key: group.id // 确保每个 group 有唯一的 key
        }));
        setGroupList(groupsWithKey);


    }

    useEffect(() => {
        console.log("Options updated:", option);
    }, [option]);
    useEffect(() => {
        console.log("selectValue updated:", selectValue);
        if (selectValue) {
            getGroupList()
        }

    }, [selectValue]);
    useEffect(() => {
        document.title = '群组管理';
        request().then(r => {})

    }, []);
    const columns = [
        {
            title: "id",
            dataIndex: "id",
            key: "id"

        },
        {
            title: "群组名称",
            dataIndex: "group_name",
            key: "group_name"
        },
        {
            title: "群组id",
            dataIndex: "group_id",
            key: "group_id"
        },
        {
            title: "群组类型",
            dataIndex: "group_type",
            key: "group_type",


        }
    ]
    const handleChange = (value)=>{
        console.log("selectValue:",value);
        setSelectValue(value);

    }
    return (
        <div >
            <Select
            onChange={handleChange}
            options={option}
            defaultValue={defaultSelectValue}
            placeholder="请选择"
            value={selectValue}
            className={"w-52 m-2"}
            />

            <Button
                onClick={syncGroupList}
                className={"m-2"}
                >同步用户群组</Button>

            <Table
                className={"m-2"}
                columns={columns}
                dataSource={groupList}
            >

            </Table>
        </div>
    );
}
