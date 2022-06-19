<template>
    <section class="chart-container">
        <el-row>
            <el-col :span="12">
                <el-table :data="tableData" style="width: 100%" max-height="400" :default-sort = "{prop: 'date', order: 'descending'}">
                  <el-table-column prop="commit_id" label="Commit ID" sortable width="200">
                  </el-table-column>
                  <el-table-column prop="repo_name" label="Warehouse Name" sortable width="100">
                  </el-table-column>
                  <el-table-column prop="author" label="Author" width="160">
                  </el-table-column>
                  <el-table-column prop="commit_time" label="Time" width="110">
                  </el-table-column>
                </el-table>
            </el-col>
            <el-col :span="12">
                <div id="chartPie" style="width:100%; height:400px;"></div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
import echarts from "echarts";
import { getCommitPieChart,getNewCommits } from "../../api/api";
export default {
  data() {
    return {
      chartPie: null,
      tableData: []  
    }
  },

  methods: {
    formatter(row, column) {
        return row.address;
    },
    drawPieChart() {
      this.chartPie = echarts.init(document.getElementById("chartPie"));
      getCommitPieChart().then(res => {
        let { value, code, total,repo } = res.data;
        console.log(repo)
        console.log(value)
        var temp=new Array()
        var i=0;
        for(i=0;i<value.length;i++){
          temp[i]={value:value[i].commit_num,name:value[i].repo_name}
        }
        console.log(temp)
        if (code !== 200) {
          this.$message({
            message: "服务端发生错误",
            type: "warning"
          });
        } else {
          this.chartPie.setOption({
            title: {
              text: "The Number of Commit per Warehouse",
              subtext: "Total Number:" + total,
              x: "center"
            },
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
              orient: "vertical",
              left: "left",
              data: repo// 和value一一对应
            },
            toolbox: {
              show: true,
              feature: {
                saveAsImage: { show: true }
              }
            },
            series: [
              {
                name: "proportion",
                type: "pie",
                radius: "55%",
                center: ["50%", "60%"],
                data: temp,
                itemStyle: {
                  emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)"
                  }
                }
              }
            ]
          });
        }
      });
    },
    getNewCommitTable() {
      getNewCommits().then(res => {
        console.log(11)
        this.tableData = res.data.Commits;
      });
    },
    drawCharts() {
      // console.log(echarts.version)
      this.drawPieChart();
      this.getNewCommitTable();
    }
  },

  mounted: function() {
    this.drawCharts();
  },
  // updated: function() {
  //   this.drawCharts();
  // }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  float: left;
}
/*.chart div {
        height: 400px;
        float: left;
    }*/

.el-col {
  padding: 30px 20px;
}
</style>
