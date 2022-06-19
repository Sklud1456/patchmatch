import Login from './views/Login.vue'
import NotFound from './views/404.vue'
import Home from './views/Home.vue'
import Table from './views/nav1/Table.vue'
import echarts from './views/charts/echarts.vue'
import CommitTable from './views/nav1/CommitTable.vue'
import CVETable from './views/nav1/CVETable.vue'
import CVEChart from './views/charts/CVEChart.vue'
import CommitChart from './views/charts/Commitchart.vue'
import Hometest from './views/Hometest.vue'
import Predict from './views/Predict.vue'

let routes = [
    // {
    //     path: '/login',
    //     component: Login,
    //     name: '',
    //     hidden: true
    // },
    // {
    //     path: '/404',
    //     component: NotFound,
    //     name: '',
    //     hidden: true
    // },
    //{ path: '/main', component: Main },
    // {
    //     path: '/',
    //     component: Home,
    //     name: 'Table',
    //     leaf: true,//只有一个节点
    //     iconCls: 'fa fa-id-card-o',//图标样式class
    //     children: [
    //         { path: '/table', component: Table, name: '信息汇总' },
    //     ]
    // },
    // {
    //     path: '/',
    //     component: Home,
    //     name: 'Charts',
    //     leaf: true,
    //     iconCls: 'fa fa-bar-chart',
    //     children: [
    //         { path: '/echarts', component: echarts, name: '图表展示' }
    //     ]
    // },
    {
        path: '/predict',
        component: Predict,
        name: 'PredictCommitForCVE',
        hidden: true
    },
    {
        path: '/',
        component: Hometest,
        name: 'ChartCVE',
        leaf: true,
        iconCls: 'fa fa-id-card-o',
        children: [
            { path: '/CVEchart', component: CVEChart, name: 'CVE Information' }
        ]
    },
    {
        path: '/',
        component: Hometest,
        name: 'ChartCommit',
        leaf: true,
        iconCls: 'fa fa-id-card-o',
        children: [
            { path: '/Commitchart', component: CommitChart, name: 'Commit Information' }
        ]
    },
    {
        path: '/',
        component: Hometest,
        name: 'TableCommit',
        leaf: true,
        iconCls: 'fa fa-bar-chart',
        children: [
            { path: '/committable', component: CommitTable, name: 'Commit List' }
        ]
    },
    {
        path: '/',
        component: Hometest,
        name: 'TableCVE',
        leaf: true,
        iconCls: 'fa fa-bar-chart',
        children: [
            { path: '/CVEtable', component: CVETable, name: 'CVE List' }
        ]
    },
    

    // {
    //     path: '*',
    //     hidden: true,
    //     redirect: { path: '/404' }
    // }
];

export default routes;