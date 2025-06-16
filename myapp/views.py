from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from manim import *
import os
import json
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveAPIView,RetrieveDestroyAPIView,ListAPIView
from .models import Article,Slides,Test,TestResult,SlidesPdf,ArticlePdf
from .serializers import ArticleSerializer,SlideSerializer,TestSerializer,TestResultSerializer,SlidesPdfSerializer,ArticlePdfSerializer
import random
from docx import Document
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsOwner
from django.contrib.auth.models import User
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


# Nazariy ma'lumotlar

class MyModelRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
class PdfRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = ArticlePdf.objects.all()
    serializer_class = ArticlePdfSerializer
class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'  
class ArticleListAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
class ArticleCreateView(CreateAPIView):
    queryset=Article.objects.all()
    serializer_class=ArticleSerializer
class ArticleUploadPdfView(CreateAPIView):
    queryset = ArticlePdf.objects.all()
    serializer_class = ArticlePdfSerializer
    parser_classes = (MultiPartParser, FormParser)  # Fayllarni qabul qilish uchun parserlar

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Saving the instance without user
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
class ArticleListPdfView(APIView):
    def get(self, request):
        articles = ArticlePdf.objects.all()
        serializer = ArticlePdfSerializer(articles, many=True)
        return Response(serializer.data)




# Taqdimotlar

class SlideRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = Slides.objects.all()
    serializer_class = SlideSerializer
class SlideDetailView(RetrieveAPIView):
    queryset = Slides.objects.all()
    serializer_class = SlideSerializer
    lookup_field = 'id'  
class SlideListAPIView(APIView):
    def get(self, request):
        articles = Slides.objects.all()
        serializer = SlideSerializer(articles, many=True)
        return Response(serializer.data)
class SlideCreateView(CreateAPIView):
    queryset=Slides.objects.all()
    serializer_class=SlideSerializer
class SlideUploadPdfView(CreateAPIView):
    queryset = SlidesPdf.objects.all()
    serializer_class = SlidesPdfSerializer
    parser_classes = (MultiPartParser, FormParser)  # Fayllarni qabul qilish uchun parserlar

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Saving the instance without user
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
class SlideListPdfView(APIView):
    def get(self, request):
        articles = SlidesPdf.objects.all()
        serializer = SlidesPdfSerializer(articles, many=True)
        return Response(serializer.data)

# Test

class TestRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
def parse_test_file(file_path):
    ans = {}
    content = []

    # Faylning kengaytmasini aniqlash
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.docx':
        document = Document(file_path)
        # DOCX hujjatidagi har bir paragrafni o'qish
        for para in document.paragraphs:
            content.append(para.text)
        content = "\n".join(content).split("++++")
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().split("++++")

    # Random bo'laklar tayyorlash
    f2 = random.sample(content, k=len(content))
    for item in f2:
        savol = item.split('====')
        s = savol[0].strip()
        variants = savol[1:]

        variant = random.sample(variants, k=min(4, len(variants)))
        dc = {}
        for j in variant:
            j = j.strip()
            if j.startswith('#'):
                dc[j[1:]] = True
            else:
                dc[j] = False
        ans[s] = dc

    return ans
class TestDetailView(RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.file.path if instance.file else None

        if file_path and os.path.exists(file_path):
            ans = parse_test_file(file_path)
        else:
            ans = {}

        
        return Response(ans)
class TestListAPIView(APIView):
    def get(self, request):
        articles = Test.objects.all()
        serializer = TestSerializer(articles, many=True)
        return Response(serializer.data)
class TestCreateView(CreateAPIView):
    queryset=Test.objects.all()
    serializer_class=TestSerializer
    
class SaveTestResultView(APIView):
    def post(self, request):
        # Extract data from the request
        user_id = request.data.get('user_id')
        test_id = request.data.get('test_id')
        score = request.data.get('score')
        total_questions = request.data.get('total_questions')

        # Create a new TestResult instance and save it
        test_result = TestResult.objects.create(
            user_id=user_id,
            test_id=test_id,
            score=score,
            total_questions=total_questions
        )

        return Response({"message": "Test result saved!", "test_result_id": test_result.id}, status=status.HTTP_201_CREATED)
class TestResultListView(ListAPIView):
    serializer_class = TestResultSerializer
    

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            try:
                return TestResult.objects.filter(user__id=user_id)
            except ValueError:
                return TestResult.objects.none()  # Agar user_id noto'g'ri formatda bo'lsa
        return TestResult.objects.none()
# 

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Tokenlarni olish
        tokens = serializer.validated_data

        # Foydalanuvchi ob'ektini olish
        user = serializer.user
        
        # Foydalanuvchining superuser yoki staff ekanligini tekshirish
        is_superuser = user.is_superuser
        is_staff = user.is_staff

        # Tokenlarga qo'shimcha ma'lumot qo'shish
        tokens['is_superuser'] = is_superuser
        tokens['is_staff'] = is_staff
        tokens['user_id'] = user.id

        return Response(tokens, status=status.HTTP_200_OK)
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Faqat autentifikatsiyalangan foydalanuvchilar uchun

    def get(self, request):
        # Token to'g'ri bo'lsa, bu ma'lumot qaytariladi
        return Response({"message": "Bu himoyalangan yo'lga kirdingiz!"}, status=200)
class LimitGraph(MovingCameraScene):
    def __init__(self, epsilon): 
        self.epsilon = epsilon
        super().__init__()

    def construct(self):
        epsilon = abs(self.epsilon)
        delta = min(epsilon / 5, 1)
        formula_info = MathTex(
            r"\lim_{x \to 2} x^2 = 4, \quad \varepsilon = " + str(epsilon) + 
            r", \quad \delta = " + str(epsilon/5),
            font_size=24
        ).to_edge(UP).shift(RIGHT*0.5 )
        
        self.play(Write(formula_info), run_time=2)
        self.wait(1)
        a = 2
        L = 4
        ysd = min(0, L - epsilon) - 1
        xsd = min(0, a - delta) - 1

        axes = Axes(
            x_range=[xsd, a + delta + 1, 1],  # X o'qidagi qadamni 1 qilib belgilash
            y_range=[ysd, L + epsilon + 1, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": BLUE},
            x_axis_config={ "include_numbers": False, },
            y_axis_config={ "include_numbers": False, },
        )

        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        graph = axes.plot(lambda x: x ** 2, color=YELLOW)

        x_left = a - delta
        x_right = a + delta
        y_lower = L - epsilon
        y_upper = L + epsilon

        # To'g'ri to'rtburchak chiziqlari
        x_delta_left_line = axes.get_vertical_line(axes.c2p(x_left, y_upper), color=GREEN, line_func=DashedLine)
        x_delta_right_line = axes.get_vertical_line(axes.c2p(x_right, y_upper), color=GREEN, line_func=DashedLine)
        y_delta_lower_line = axes.get_horizontal_line(axes.c2p(x_right, y_lower), color=RED, line_func=DashedLine, stroke_width = 2)
        y_delta_upper_line = axes.get_horizontal_line(axes.c2p(x_right, y_upper), color=RED, line_func=DashedLine,stroke_width = 2)
        

        # Axes, graph, and labels
        self.play(Create(axes), Write(labels))
        self.play(Create(graph))
        self.wait(2)
        x_values = [a - delta / 2, a - delta / 4, a, a + delta / 4, a + delta / 2]
        x_values1=[x_left,a,x_right]
        x_labels = VGroup()
        for cont, x in enumerate(x_values1):
            x_decimal = DecimalNumber(x, num_decimal_places=2, font_size=10)
            if cont % 2 == 1:
                x_decimal.next_to(axes.c2p(x, 0), UP*0.1)
            else:
                x_decimal.next_to(axes.c2p(x, 0), DOWN*0.1)
            x_labels.add(x_decimal)
        
        self.play(Write(x_labels))
        y_values = [y_lower, L, y_upper]
        y_labels = VGroup()
        for y in y_values:
            y_decimal = DecimalNumber(y, num_decimal_places=2, font_size=10)
            y_decimal.next_to(axes.c2p(0, y), LEFT)
            y_labels.add(y_decimal)
        
        self.play(Write(y_labels))
        # Chiziqlarni yaratish
        
        self.play(Create(y_delta_lower_line), Create(y_delta_upper_line))
        self.play(Create(x_delta_left_line), Create(x_delta_right_line))

        # To'rtburchakni yaratish
        

        # Nuqtalarni qo'shish
        points = [
            axes.c2p(a - delta / 2, (a - delta / 2)**2),
            axes.c2p(a - delta / 4, (a - delta / 4)**2),
            axes.c2p(a, a ** 2),
            axes.c2p(a + delta / 4, (a + delta / 4)**2),
            axes.c2p(a + delta / 2, (a + delta / 2)**2),
        ]

        # Nuqtalar va markerlarni yaratish
        point_markers = [Dot(point, color=GREEN, radius=0.02) for point in points]
        points = [a - delta / 2 - delta / 4,a - delta / 4, a, a + delta / 4,a + delta / 2 + delta / 4]
        point_coords = [axes.c2p(x, x ** 2) for x in points]
        # Nuqtalar uchun labellarni yaratish
        point_labels = VGroup(
            MathTex(f"({a - delta / 2:.2f}, {(a - delta / 2) ** 2:.2f})", font_size=4)
                .next_to(point_coords[0], LEFT, buff=0.05),
            MathTex(f"({a - delta / 4:.2f}, {(a - delta / 4) ** 2:.2f})", font_size=4)
                .next_to(point_coords[1], LEFT, buff=0.05),
            MathTex(f"({a:.2f}, {a**2:.2f})", font_size=4)
                .next_to(point_coords[2], LEFT, buff=0.05),
            MathTex(f"({a + delta / 4:.2f}, {(a + delta / 4) ** 2:.2f})", font_size=4)
                .next_to(point_coords[3], LEFT, buff=0.05),
            MathTex(f"({a + delta / 2:.2f}, {(a + delta / 2) ** 2:.2f})", font_size=4)
                .next_to(point_coords[4], LEFT, buff=0.05),
        )
        
        # Nuqtalar va markerlar bilan labellarni yaratish
        self.play(Create(VGroup(*point_markers)))
        self.play(Create(VGroup(*point_labels)))  # Labellarni qo'shish
        self.wait(2)
        rectangle = Rectangle(
            width=2 * delta, height=2 * epsilon, color=WHITE, fill_opacity=0.3
        ).move_to(axes.c2p(a, L))  # To'rtburchakni to'g'ri joylashtirish

        # Kamerani to'rtburchak ustiga yurgizish (yaqinlashtirish darajasini kamaytirish)
        self.play(self.camera.frame.animate.move_to(rectangle).set(width=rectangle.width * 14.5), run_time=4)  # Kattalashtirish darajasini kamaytirdik
        self.wait(2)
        # X-axis labels
        

        # Y-axis labels


        # Kamerani qaytarish
        self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=14))
        self.wait(2)

@api_view(['POST'])
def create_video(request):
    try:
        data = json.loads(request.body)
        epsilon = data.get('epsilon', 0.5)  # Agar epsilon kelmasa default 0.5

        video_output_dir = "media/videos/"
        video_filename = "limit_graph.mp4"
        video_dir="media/videos/videos/1080p60/"
        video_path = os.path.join(video_dir, video_filename)

        if not os.path.exists(video_output_dir):
            os.makedirs(video_output_dir)

        # Manim konfiguratsiyasi
        config.media_dir = video_output_dir  
        config.output_file = video_filename 

        # LimitGraph sinfini epsilon bilan yaratish
        scene = LimitGraph(epsilon)
        scene.render()

        # Yaratilgan videoni qaytarish
        video_url = request.build_absolute_uri(video_path)  # URL manzilini olish
        return JsonResponse({"status": "Video created!", "video_path": video_path})
    except Exception as e:
        return JsonResponse({"status": "Error occurred", "message": str(e)})
class CustomPlotExample(Scene):
    def __init__(self, epsilon, x_end):
        self.epsilon = epsilon
        self.x_end = x_end
        super().__init__()

    def construct(self):
        epsilon = abs(self.epsilon)
        x_end = abs(self.x_end)

        # Koordinata o'qi
        plot_axes = Axes(
            x_range=[0, x_end + 1, 1],
            y_range=[-1.1, 1.1, 0.1],
            x_length=8,
            y_length=4,
            axis_config={"font_size": 8},
            tips=False,
        )
        y_label = plot_axes.get_y_axis_label("x_n", edge=LEFT, direction=LEFT).shift(UP*2)
        x_label = plot_axes.get_x_axis_label("n", edge=RIGHT, direction=RIGHT)
        plot_labels = VGroup(x_label, y_label)

        # Display additional information above the plot
        formula_info = MathTex(
            r"x_n = \frac{1}{n}, \quad a = 0, \quad \varepsilon = " + str(epsilon) + 
            r", \quad n_0 = " + str(1/epsilon),
            font_size=24
        ).to_edge(UP).shift(DOWN * 0.2)

        # Epsilon chiziqlar
        epsilon_line_pos = plot_axes.get_horizontal_line(plot_axes.c2p(x_end, epsilon, 0), color=RED, line_func=DashedLine)
        epsilon_line_neg = plot_axes.get_horizontal_line(plot_axes.c2p(x_end, -epsilon, 0), color=RED, line_func=DashedLine)

        epsilon_label_pos = MathTex(r"\varepsilon=" + str(epsilon), font_size=20).next_to(epsilon_line_pos, RIGHT)
        epsilon_label_neg = MathTex(r"-\varepsilon=" + str(-epsilon), font_size=20).next_to(epsilon_line_neg, RIGHT)

        # Muhim n nuqtalari
        significant_n = list(range(1, 11)) + list(range((x_end // 2) - 1, (x_end // 2) + 2)) + list(range(x_end - 2, x_end + 1))

        dots = VGroup()
        small_dots = VGroup()
        formula_display = MathTex("", font_size=24).to_edge(LEFT)
        self.play(Write(formula_info), run_time=2)
        self.play(Create(plot_axes), run_time=2)
        self.play(Create(plot_labels), run_time=2)
        self.play(Create(epsilon_line_pos), Create(epsilon_line_neg), Write(epsilon_label_pos), Write(epsilon_label_neg), run_time=2)
        

        for n in range(1, x_end + 1):
            x_val = n
            y_val = 1 / n
            color = RED if abs(y_val) >= epsilon else BLUE

            if n in significant_n:
                dot = Dot(plot_axes.c2p(x_val, y_val, 0), radius=0.035, color=color)
                dots.add(dot)
                formula = MathTex(f"x_{{{n}}} = \\frac{{1}}{{{n}}}", font_size=24).to_edge(LEFT).shift(UP * 0.2)
                self.play(Create(dot), Transform(formula_display, formula), run_time=0.8)
                self.wait(0.5)
                x_value_display = MathTex(f"x_{{{n}}}", font_size=20).next_to(dot, UP*0.2)  # X qiymatini ko'rsatish
                self.play(Write(x_value_display), run_time=0.5)
                self.wait(0.5)  # Har bir nuqtadan keyin to'xtash
                self.play(FadeOut(x_value_display))
            else:
                small_dot = Dot(plot_axes.c2p(x_val, y_val, 0), radius=0.02, color=GRAY)
                small_dots.add(small_dot)
                self.play(Create(small_dot), run_time=0.2)

        self.play(Create(small_dots), run_time=1)
        self.wait(2)
# Django API funksiya
@api_view(['POST'])
def create_custom_plot_video(request):
    try:
        # Foydalanuvchidan kelgan ma'lumotlarni o'qish
        data = json.loads(request.body)
        epsilon = float(data.get('epsilon', 1))  # Agar epsilon kelmasa default qiymat
        x_end = int(data.get('x_end', 20))

        # Video fayllar uchun katalog
        video_output_dir = "media/videos/"
        video_filename = "custom_plot_example.mp4"
        video_dir="media/videos/videos/1080p60/"
        video_path = os.path.join(video_dir, video_filename)

        # Katalog mavjudligini tekshirish, agar bo'lmasa yaratish
        if not os.path.exists(video_output_dir):
            os.makedirs(video_output_dir)

        # Manim sozlamalari
        config.media_dir = video_output_dir  
        config.output_file = video_filename  

        # Grafikni yaratish
        scene = CustomPlotExample(epsilon, x_end)
        scene.render()

        # Yaratilgan videoni qaytarish
        video_url = request.build_absolute_uri(video_path)  # URL manzilini olish
        return JsonResponse({"status": "Video created!", "video_path": video_path})
    
    except Exception as e:
        return JsonResponse({"status": "Error occurred", "message": str(e)})