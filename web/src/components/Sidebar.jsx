'use client'
import React from 'react';
import { Menu } from 'antd';
import { HomeOutlined, DashboardOutlined, SettingOutlined } from '@ant-design/icons';
import Link from 'next/link';
import AccountsPool from "@/app/accountsPool/page";
import { usePathname } from 'next/navigation';


const  items = [

];


const Sidebar = () => {
    const pathname = usePathname();
    return (
        <Menu
            style={{ height: '100%', borderRight: 0 }}
            mode="inline"
            defaultSelectedKeys={['/']}
            selectedKeys={[pathname]} // 动态确定选中的菜单项

        >
            <Menu.Item key="/" icon={<HomeOutlined />}>
                <Link href="/">Home</Link>
            </Menu.Item>
            <Menu.Item key="/dashboard" icon={<DashboardOutlined />}>
                <Link href="/dashboard">Dashboard</Link>
            </Menu.Item>

            <Menu.Item key="/accountsPool" icon={<DashboardOutlined />}>
                <Link href="/accountsPool">AccountsPool</Link>
            </Menu.Item>
            <Menu.Item key="/group" icon={<DashboardOutlined />}>
                <Link href="/group">GRoup</Link>
            </Menu.Item>
            <Menu.Item key="/replayTask" icon={<DashboardOutlined />}>
                <Link href="/replayTask">replayTask</Link>
            </Menu.Item>
        </Menu>
    );
};

export default Sidebar;