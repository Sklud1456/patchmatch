<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.des" placeholder="commit description"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="getUsers">inquire</el-button>
				</el-form-item>
         <el-form-item label="Warehouse Name" prop="reponame">
          <el-select v-model="filters.repoid" placeholder="Please choose the warehouse name">
            <el-option
              v-for="item in reponameoptions"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
					<el-button type="success" @click="getUsers()">Filter</el-button>
				</el-form-item>
        <el-form-item>
					<el-button type="success" :disabled="filters.repoid==0" @click="addCommit()">Update Commit</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<!--列表-->
		<el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection" width="55">
			</el-table-column>
			<el-table-column prop="author" label="Author" width="200" sortable>
			</el-table-column>
      <el-table-column prop="commit_id" label="Commit ID" width="350" sortable>
			</el-table-column>
			<el-table-column prop="repo_name" label="Warehouse Name" width="180" sortable>
			</el-table-column>
			<el-table-column prop="commit_time" label="Committed Time" width="200" sortable>
			</el-table-column>
			<el-table-column label="Operation" width="150">
				<template scope="scope">
					<el-button size="small" @click="handleEdit(scope.$index, scope.row)">Details</el-button>
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
		<el-dialog title="Details" :visible.sync="detailFormVisible" :close-on-click-modal="false">
			<el-form :model="detailForm" label-width="80px" :rules="detailFormRules" ref="detailForm">
        <el-form-item label="Commit ID" prop="commit_id">
							<el-input v-model="detailForm.commit_id" auto-complete="off"></el-input>
						</el-form-item>
				<el-row>
            <el-col :span="12">
  						<el-form-item label="Warehouse Name">
							<el-input v-model="detailForm.repo_name"></el-input>
						</el-form-item>
  					</el-col>
  					<el-col :span="12">
  						<el-form-item label="Author">
							<el-input v-model="detailForm.author"></el-input>
						</el-form-item>
  					</el-col>
				</el-row>
				<el-row>
  					<el-col :span="30">
  						<el-form-item label="Commit Time">
							<el-input v-model="detailForm.commit_time" auto-complete="off"></el-input>
						</el-form-item>
  					</el-col>
				</el-row>
				<el-form-item label="Detials">
					<el-input type="textarea" v-model="detailForm.description"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="detailFormVisible = false">Back</el-button>
			</div>
		</el-dialog>

    <!-- 提示信息 -->
    <el-dialog title="Reminder" :visible.sync="addCommitError" width="30%">
      <el-row :gutter="15">
      <span>The warehouse is up to date</span>
      </el-row>
      <span slot="footer" class="dialog-footer">
        <!-- <el-button @click="checktocommitOK = false">取 消</el-button> -->
        <el-button type="primary" @click.native="addCommitError = false">OK</el-button>
      </span>
    </el-dialog>

    <!-- 提示信息 -->
    <el-dialog title="Reminder" :visible.sync="addCommitOK" width="30%">
      <el-row :gutter="15">
      <span>Update Commit successed</span>
      </el-row>
      <el-row :gutter="15">
      <span>Add Commit:{{addnum}}</span>
      </el-row>
      <el-row :gutter="15">
      <span>Commits:{{commitlist}}</span>
      </el-row>
      <span slot="footer" class="dialog-footer">
        <!-- <el-button @click="checktocommitOK = false">取 消</el-button> -->
        <el-button type="primary" @click.native="addCommitOK = false">OK</el-button>
      </span>
    </el-dialog>

	</section>
</template>

<script>
import util from "../../common/js/util";
import { getCommitListPage, removeUser, batchRemoveUser,addNewCommit } from "../../api/api";

export default {
  data() {
    return {
      filters: {
        des: "",
        repoid:""
      },
      users: [],
      page_size: 20,
      total: 0,
      page: 1,
      listLoading: false,
      sels: [], //列表选中列

      detailFormVisible: false, //详情界面是否显示
      addCommitError:false,//新增失败
      addCommitOK:false,//新增成功
      editLoading: false,


      commitlist:"",
      addnum:0,
      detailFormRules: {
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }]
      },
      //详情界面数据
      detailForm: {
        id: 0,
        name: "",
        profess: "",
        grade: 0,
        phone: 0,
        email: "",
        group: "",
        pub_data: "",
        power: ""
      },
      code:0,
      reponameoptions: [{
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
    testit(){
      console.log(this.reponame)
    },
    handleCurrentChange(val) {
      this.page = val;
      this.getUsers();
    },
    //获取用户列表
    getUsers() {
      
      let para = {
        page: this.page,
        des: this.filters.des,
        repoid:this.filters.repoid
      };
      this.listLoading = true;
      // NProgress.start();
      getCommitListPage(para).then(res => {
        this.total = res.data.total;
        this.page_size = res.data.page_size;
        this.users = res.data.infos;
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
            this.getUsers();
          });
        })
        .catch(() => {});
    },
    //显示详情界面
    handleEdit: function(index, row) {
      this.detailFormVisible = true;
      this.detailForm = Object.assign({}, row);
    },
    //新增commit
    addCommit: function() {
      let para = {
        repoid: this.filters.repoid
      };
      console.log(para)
      this.listLoading = true;
      // NProgress.start();
      addNewCommit(para).then(res => {
        this.code = res.data.code;
        this.backmsg = res.data.infos;
        this.addnum = res.data.nums;
        this.commitlist=res.data.commits;
        this.listLoading = false;
        if(this.code==500){
          this.addCommitError=true;
        }
        else if(this.code=200){
          this.addCommitOK=true;
        }
      });
      

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
            this.getUsers();
          });
        })
        .catch(() => {});
    }
  },
  mounted() {
    this.getUsers();
  }
};
</script>

<style scoped>

</style>