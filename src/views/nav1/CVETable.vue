<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.CVE" placeholder="CVE ID"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="getCVEs">inquire</el-button>
				</el-form-item>
        <el-form-item label="Warehouse Name" prop="reponame">
          <el-select v-model="filters.repoid" placeholder="Please choose warehouse name">
            <el-option
              v-for="item in reponameoptions"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
					<el-button type="success" v-on:click="getCVEs()">Filter</el-button>
				</el-form-item>
        <el-form-item>
					<el-button type="success" v-on:click="newCVE">Add CVE</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<!--列表-->
		<el-table :data="CVEs" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection" width="55">
			</el-table-column>
			<el-table-column prop="CVE_id" label="CVE" width="100" sortable>
			</el-table-column>
      <el-table-column prop="cvetime" label="Time" width="115" sortable>
			</el-table-column>
			<el-table-column prop="repo_name" label="Warehouse Name" width="180" sortable>
			</el-table-column>
			<el-table-column prop="patch_gitcommit" label="Patched Commit" width="195" sortable>
			</el-table-column>
			<el-table-column prop="score" label="Risk Score" width="130" sortable>
      </el-table-column>
			<el-table-column prop="S_des" label="Risk Type" width="125" sortable>
      </el-table-column>
			<el-table-column prop="cwe_id" label="CWE" width="100" sortable>
      </el-table-column>
			<el-table-column prop="cwe_name" label="CWE type" width="160" sortable>
      </el-table-column>
			<el-table-column label="Operation" width="120">
				<template scope="scope">
					<el-button :type="buttonType(scope.row.patch_gitcommit)" size="small" @click="handleEdit(scope.$index, scope.row)">Detials</el-button>
          <!-- <el-button :type="buttonType(CVEs.patch_gitcommit)" size="small" @click="handleEdit(scope.$index, scope.row)">详情</el-button> -->
					<!-- <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button> -->
				</template>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<!-- <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button> -->
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="page_size" :total="total" style="float:right;">
			</el-pagination>
		</el-col>

		<!--详情界面-->
		<el-dialog title="Detials" :visible.sync="detailFormVisible" :close-on-click-modal=false>
			<el-form :model="detailForm" label-width="80px" :rules="detailFormRules" ref="detailForm">
        <el-form-item label="CVE_id" prop="CVE">
							<el-input v-model="detailForm.CVE_id" auto-complete="off"></el-input>
						</el-form-item>
				<el-row>
            <el-col :span="12">
  						<el-form-item label="Warehouse Name">
							<el-input v-model="detailForm.repo_name"></el-input>
						</el-form-item>
  					</el-col>
  					<el-col :span="12">
  						<el-form-item label="Commit Time">
							<el-input v-model="detailForm.cvetime"></el-input>
						</el-form-item>
  					</el-col>
				</el-row>
				<el-row>
  					<el-col :span="30">
  						<el-form-item label="COMMIT">
							<el-input v-model="detailForm.patch_gitcommit" auto-complete="off"></el-input>
						</el-form-item>
  					</el-col>
				</el-row>
        <el-row>
            <el-col :span="12">
  						<el-form-item label="Phase Type">
							<el-input v-model="detailForm.Status"></el-input>
						</el-form-item>
  					</el-col>
  					<el-col :span="12">
  						<el-form-item label="Phase">
							<el-input v-model="detailForm.Phase"></el-input>
						</el-form-item>
  					</el-col>
				</el-row>
				<el-form-item label="description">
					<el-input type="textarea" v-model="detailForm.Description"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="jump(detailForm.CVE_id)" v-if='detailForm.patch_gitcommit==""||detailForm.patch_gitcommit==null'>Predict Commit</el-button>
        <!-- <el-button @click="show(detailForm.patch_gitcommit)" v-if='detailForm.patch_gitcommit!=null'>预测commit</el-button> -->
				<el-button @click.native="detailFormVisible = false">Back</el-button>
			</div>
		</el-dialog>

    <!-- 新增界面 -->
    <el-dialog title="ADD" :visible.sync="newCVEFormVisible" :close-on-click-modal=false>
      <el-row :gutter="15">
        <el-form ref="elForm" :model="newCVEForm" :rules="newCVEFormRules" size="medium" label-width="100px">
          <el-col :span="23">
            <el-form-item label="CVE" prop="CVE">
              <el-input v-model="newCVEForm.CVE" placeholder="please enter CVE-ID" :maxlength="50" clearable
                        prefix-icon='el-icon-user-solid' ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="23">
            <el-form-item label="Warehouse Name" prop="reponame">
              <el-select v-model="newCVEForm.repoid" placeholder="plase choose warehouse name">
                <el-option
                  v-for="item in reponameoptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-form>
      </el-row>
      <div slot="footer">
          <el-button @click.native="newCVEFormVisible = false">BACK</el-button>
          <el-button type="primary" @click="addCVE">OK</el-button>
      </div>
		</el-dialog>
    
    <!-- 提示信息 -->
    <el-dialog title="Reminder" :visible.sync="addCVEOKVisible" width="30%">
      <span>Add successed</span>
      <span slot="footer" class="dialog-footer">
        <!-- <el-button @click="checktocommitOK = false">取 消</el-button> -->
        <el-button type="primary" @click="addNewCVEOK">OK</el-button>
      </span>
    </el-dialog>

	</section>
</template>

<script>
import util from "../../common/js/util";
import { getCVEListPage, removeUser, batchRemoveUser,addNewCVE } from "../../api/api";

export default {
  data() {
    return {
      filters: {
        CVE: "",
        repoid:"",
      },
      CVEs: [],
      page_size: 20,
      total: 0,
      page: 1,
      listLoading: false,
      sels: [], //列表选中列

      detailFormVisible: false, //详情界面是否显示
      newCVEFormVisible: false, //新增界面是否显示
      addCVEOKVisible:false,
      editLoading: false,
      detailFormRules: {
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }]
      },
      //详情界面数据
      detailForm: {},
      //新增界面数据
      newCVEForm:{},
      newCVEFormRules: {
        CVE: [{ required: true, message: "请输入CVE编号", trigger: "blur" }]
      },
      backmsg:"",
      reponamefilteroptions: [{
          value: '1',
          label: 'FFmpeg'
        }, {
          value: '2',
          label: 'ImageMagick'
        }, {
          value: '3',
          label: 'jenkins'
        }, {
          value: '4',
          label: 'linux'
        }, {
          value: '5',
          label: 'moodle'
        }, {
          value: '6',
          label: 'openssl'
        }, {
          value: '7',
          label: 'php-src'
        }, {
          value: '8',
          label: 'phpmyadmin'
        }, {
          value: '9',
          label: 'qemu'
        }, {
          value: '10',
          label: 'wireshark'
        }],
      reponameoptions: [
        {
          value: '0',
          label: 'all'
        },{
          value: '1',
          label: 'FFmpeg'
        }, {
          value: '2',
          label: 'ImageMagick'
        }, {
          value: '3',
          label: 'jenkins'
        }, {
          value: '4',
          label: 'linux'
        }, {
          value: '5',
          label: 'moodle'
        }, {
          value: '6',
          label: 'openssl'
        }, {
          value: '7',
          label: 'php-src'
        }, {
          value: '8',
          label: 'phpmyadmin'
        }, {
          value: '9',
          label: 'qemu'
        }, {
          value: '10',
          label: 'wireshark'
        }],
    };
  },
  methods: {
    buttonType(str){
      if(str==""||str==null){
        return "warning";
      }
      else{
        return "success";
      }
    },
    jump(msg){
      console.log(msg)
       this.$router.push({  
            path: '/predict',   
            name: 'PredictCommitForCVE',  
            params: {   
                datacve: msg,   
            }  
        })  
      
    },
    handleCurrentChange(val) {
      this.page = val;
      this.getCVEs();
    },
    //获取CVE列表
    getCVEs() {
      let para = {
        page: this.page,
        CVE: this.filters.CVE,
        repoid:this.filters.repoid
      };
      this.listLoading = true;
      // NProgress.start();
      getCVEListPage(para).then(res => {
        this.total = res.data.total;
        this.page_size = res.data.page_size;
        this.CVEs = res.data.infos;
        // console.log(res.data.infos);
        this.listLoading = false;
      });
    },
    //删除
    handleDel: function(index, row) {
      this.$confirm("确认删除该用户吗?", "提示", {
        type: "warning"
      })
        .then(() => {
          this.listLoading = true;
          //NProgress.start();
          let para = { id: row.id };
          removeUser(para).then(res => {
            this.listLoading = false;
            let { msg, code } = res.data;
            if (code !== 200) {
              this.$message({
                message: msg,
                type: "warning"
              });
            } else {
              this.$message({
                message: msg,
                type: "success"
              });
            }
            this.getCVEs();
          });
        })
        .catch(() => {});
    },
    //显示详情界面
    handleEdit: function(index, row) {
      this.detailFormVisible = true;
      this.detailForm = Object.assign({}, row);
    },
    //显示新增界面
    newCVE: function(index, row) {
      this.newCVEFormVisible = true;
    },
    //新增CVE提交
    addCVE: function() {
      let para = {
        CVE: this.newCVEForm.CVE,
        repoid: this.newCVEForm.repoid
      };
      console.log(para)
      // this.listLoading = true;
      // NProgress.start();
      addNewCVE(para).then(res => {
        this.backmsg = res.data.infos;
        // this.listLoading = false;
      });
      this.newCVEFormVisible=false
      this.addCVEOKVisible=true
      // console.log(this.backmsg)

    },
    addNewCVEOK: function() {
      this.addCVEOKVisible=false;
      this.getCVEs();
    },
    selsChange: function(sels) {
      this.sels = sels;
    },
    //批量删除
    batchRemove: function() {
      var ids = this.sels.map(item => item.id).toString();
      this.$confirm("确认删除选中用户吗？", "提示", {
        type: "warning"
      })
        .then(() => {
          this.listLoading = true;
          let para = { ids: ids };
          batchRemoveUser(para).then(res => {
            this.listLoading = false;
            let { msg, code } = res.data;
            if (code !== 200) {
              this.$message({
                message: msg,
                type: "warning"
              });
            } else {
              this.$message({
                message: msg,
                type: "success"
              });
            }
            this.getCVEs();
          });
        })
        .catch(() => {});
    }
  },
  mounted() {
    this.getCVEs();
  }
};
</script>

<style scoped>

</style>