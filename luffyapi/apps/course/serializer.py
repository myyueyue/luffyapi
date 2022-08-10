'''
 @Description:见字如面 
 @Author: MING
 @Title: 
 @Date: 2022/8/7 9:20
'''
from rest_framework import serializers

from . import models


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id', 'name']


class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['name', 'role_name', 'title', 'signature', 'image', 'brief']


class CourseModelSerializer(serializers.ModelSerializer):
    # 子序列化
    teacher = TeacherModelSerializer()

    class Meta:
        model = models.Course
        fields = ['id',
                  'name',
                  'course_img',
                  'brief',
                  'attachment_path',
                  'pub_sections',
                  'price',
                  'students',
                  'period',
                  'sections',
                  'course_type_name',
                  'level_name',
                  'status_name',
                  'teacher',
                  'section_list',
                  ]


class CourseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseSection
        fields = ['name', 'orders', 'duration', 'free_trail', 'section_link', 'section_type_name']


class CourseChapterModelSerializer(serializers.ModelSerializer):
    #章节多课时
    coursesections = CourseChapterSerializer(many=True)

    class Meta:
        model = models.CourseChapter
        fields = ['chapter', 'name', 'summary', 'coursesections']


