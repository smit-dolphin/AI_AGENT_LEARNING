<?php

namespace App\Http\Controllers\Api\V2;

use App\Http\Controllers\Controller;
use App\Services\ProductService;
use App\Repositories\ProductRepository;
use App\Http\Requests\ProductRequest;
use App\Http\Resources\ProductResource;
use App\Events\ProductUpdated;
use App\Exceptions\ProductNotFoundException;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class ProductController extends Controller
{

    /**
     * Executes the function logic.
     *
     * @return mixed
     */
    public function __construct(
        private ProductService $productService,
        private ProductRepository $productRepository
    ) {
        $this->middleware('auth:api');
        $this->middleware('role:admin')->only(['destroy', 'bulkDelete']);
        $this->middleware('throttle:60,1');
    }

    /**
     * Executes the index logic.
     *
     * @param mixed $request
     *
     * @return mixed
     */
    public function index(Request $request): JsonResponse
    {
        $perPage = $request->input('per_page', 15);
        $filters = $request->only(['category', 'status', 'price_min', 'price_max', 'tags']);
        
        $products = $this->productRepository->getFiltered($filters, $perPage);
        
        return response()->json([
            'success' => true,
            'data' => ProductResource::collection($products),
            'meta' => [
                'current_page' => $products->currentPage(),
                'total' => $products->total(),
                'per_page' => $products->perPage(),
            ],
        ]);
    }

    /**
     * Executes the store logic.
     *
     * @param mixed $request
     *
     * @return mixed
     */
    public function store(ProductRequest $request): JsonResponse
    {
        try {
            DB::beginTransaction();
            
            $validated = $request->validated();
            $product = $this->productService->createProduct($validated);
            
            if ($request->has('images')) {
                $this->productService->attachImages($product, $request->input('images'));
            }
            
            if ($request->has('variants')) {
                $this->productService->createVariants($product, $request->input('variants'));
            }
            
            Cache::tags(['products'])->flush();
            
            DB::commit();
            
            return response()->json([
                'success' => true,
                'message' => 'Product created successfully',
                'data' => new ProductResource($product),
            ], 201);
            
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Product creation failed: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => 'Failed to create product',
                'error' => config('app.debug') ? $e->getMessage() : null,
            ], 500);
        }
    }

    /**
     * Executes the show logic.
     *
     * @param mixed $id
     *
     * @return mixed
     */
    public function show(string $id): JsonResponse
    {
        $cacheKey = "product:{$id}";
        
        $product = Cache::tags(['products'])->remember($cacheKey, 3600, function () use ($id) {
            return $this->productRepository->findWithRelations($id, ['category', 'variants', 'images']);
        });
        
        if (!$product) {
            throw new ProductNotFoundException("Product with ID {$id} not found");
        }
        
        return response()->json([
            'success' => true,
            'data' => new ProductResource($product),
        ]);
    }

    /**
     * Executes the update logic.
     *
     * @param mixed $request
     * @param mixed $id
     *
     * @return mixed
     */
    public function update(ProductRequest $request, string $id): JsonResponse
    {
        try {
            DB::beginTransaction();
            
            $product = $this->productRepository->find($id);
            
            if (!$product) {
                throw new ProductNotFoundException("Product with ID {$id} not found");
            }
            
            $validated = $request->validated();
            $updatedProduct = $this->productService->updateProduct($product, $validated);
            
            if ($request->has('images')) {
                $this->productService->syncImages($updatedProduct, $request->input('images'));
            }
            
            if ($request->has('variants')) {
                $this->productService->updateVariants($updatedProduct, $request->input('variants'));
            }
            
            Cache::tags(['products'])->flush();
            Cache::forget("product:{$id}");
            
            event(new ProductUpdated($updatedProduct));
            
            DB::commit();
            
            return response()->json([
                'success' => true,
                'message' => 'Product updated successfully',
                'data' => new ProductResource($updatedProduct),
            ]);
            
        } catch (ProductNotFoundException $e) {
            DB::rollBack();
            return response()->json([
                'success' => false,
                'message' => $e->getMessage(),
            ], 404);
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Product update failed: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => 'Failed to update product',
                'error' => config('app.debug') ? $e->getMessage() : null,
            ], 500);
        }
    }

    /**
     * Executes the destroy logic.
     *
     * @param mixed $id
     *
     * @return mixed
     */
    public function destroy(string $id): JsonResponse
    {
        try {
            DB::beginTransaction();
            
            $product = $this->productRepository->find($id);
            
            if (!$product) {
                throw new ProductNotFoundException("Product with ID {$id} not found");
            }
            
            $this->productService->deleteProduct($product);
            
            Cache::tags(['products'])->flush();
            Cache::forget("product:{$id}");
            
            DB::commit();
            
            return response()->json([
                'success' => true,
                'message' => 'Product deleted successfully',
            ], 200);
            
        } catch (ProductNotFoundException $e) {
            DB::rollBack();
            return response()->json([
                'success' => false,
                'message' => $e->getMessage(),
            ], 404);
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Product deletion failed: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => 'Failed to delete product',
            ], 500);
        }
    }

    /**
     * Executes the bulkDelete logic.
     *
     * @param mixed $request
     *
     * @return mixed
     */
    public function bulkDelete(Request $request): JsonResponse
    {
        $request->validate([
            'product_ids' => 'required|array|min:1',
            'product_ids.*' => 'required|string|exists:products,id',
        ]);
        
        try {
            DB::beginTransaction();
            
            $deletedCount = $this->productService->bulkDeleteProducts($request->input('product_ids'));
            
            Cache::tags(['products'])->flush();
            
            DB::commit();
            
            return response()->json([
                'success' => true,
                'message' => "{$deletedCount} products deleted successfully",
                'data' => ['deleted_count' => $deletedCount],
            ]);
            
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Bulk deletion failed: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => 'Failed to delete products',
            ], 500);
        }
    }

    /**
     * Executes the updateStock logic.
     *
     * @param mixed $request
     * @param mixed $id
     *
     * @return mixed
     */
    public function updateStock(Request $request, string $id): JsonResponse
    {
        $request->validate([
            'stock' => 'required|integer|min:0',
            'location' => 'sometimes|string|max:50',
        ]);
        
        try {
            DB::beginTransaction();
            
            $product = $this->productRepository->find($id);
            
            if (!$product) {
                throw new ProductNotFoundException("Product with ID {$id} not found");
            }
            
            $oldStock = $product->stock;
            $newStock = $request->input('stock');
            
            $this->productService->updateStock($product, $newStock, $request->input('location'));
            
            if ($oldStock <= 0 && $newStock > 0) {
                event(new ProductBackInStock($product));
            }
            
            Cache::forget("product:{$id}");
            Cache::tags(['products'])->flush();
            
            DB::commit();
            
            return response()->json([
                'success' => true,
                'message' => 'Stock updated successfully',
                'data' => [
                    'product_id' => $id,
                    'old_stock' => $oldStock,
                    'new_stock' => $newStock,
                ],
            ]);
            
        } catch (ProductNotFoundException $e) {
            DB::rollBack();
            return response()->json([
                'success' => false,
                'message' => $e->getMessage(),
            ], 404);
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Stock update failed: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => 'Failed to update stock',
            ], 500);
        }
    }

    /**
     * Executes the search logic.
     *
     * @param mixed $request
     *
     * @return mixed
     */
    public function search(Request $request): JsonResponse
    {
        $request->validate([
            'q' => 'required|string|min:2',
            'sort_by' => 'sometimes|in:price,name,created_at,popularity',
            'sort_order' => 'sometimes|in:asc,desc',
        ]);
        
        $query = $request->input('q');
        $sortBy = $request->input('sort_by', 'popularity');
        $sortOrder = $request->input('sort_order', 'desc');
        $perPage = $request->input('per_page', 20);
        
        $cacheKey = "product_search:{$query}:{$sortBy}:{$sortOrder}:{$perPage}";
        
        $results = Cache::tags(['products', 'searches'])->remember($cacheKey, 1800, function () use ($query, $sortBy, $sortOrder, $perPage) {
            return $this->productService->searchProducts($query, $sortBy, $sortOrder, $perPage);
        });
        
        return response()->json([
            'success' => true,
            'data' => ProductResource::collection($results),
            'meta' => [
                'query' => $query,
                'total_results' => $results->total(),
                'applied_filters' => [
                    'sort_by' => $sortBy,
                    'sort_order' => $sortOrder,
                ],
            ],
        ]);
    }

    /**
     * Executes the validateAndSanitizeInput logic.
     *
     * @param mixed $data
     *
     * @return mixed
     */
    private function validateAndSanitizeInput(array $data): array
    {
        $sanitized = [];
        
        foreach ($data as $key => $value) {
            if (is_string($value)) {
                $sanitized[$key] = htmlspecialchars(trim($value), ENT_QUOTES, 'UTF-8');
            } elseif (is_array($value)) {
                $sanitized[$key] = $this->validateAndSanitizeInput($value);
            } else {
                $sanitized[$key] = $value;
            }
        }
        
        return $sanitized;
    }

    /**
     * Executes the prepareProductDataForExport logic.
     *
     * @param mixed $format
     *
     * @return mixed
     */
    protected function prepareProductDataForExport(string $format = 'json'): array|string
    {
        $products = $this->productRepository->getAllWithRelations(['category', 'variants']);
        
        $exportData = $products->map(function ($product) {
            return [
                'id' => $product->id,
                'name' => $product->name,
                'sku' => $product->sku,
                'price' => $product->price,
                'stock' => $product->stock,
                'category' => $product->category?->name,
                'variants_count' => $product->variants->count(),
                'created_at' => $product->created_at->toISOString(),
            ];
        });
        
        if ($format === 'json') {
            return $exportData->toJson();
        }
        
        return $exportData->toArray();
    }

    /**
     * Executes the logProductActivity logic.
     *
     * @param mixed $action
     * @param mixed $productId
     * @param mixed $oldData
     * @param mixed $newData
     *
     * @return mixed
     */
    private function logProductActivity(string $action, string $productId, ?array $oldData = null, ?array $newData = null): void
    {
        $logData = [
            'action' => $action,
            'product_id' => $productId,
            'user_id' => auth()->id(),
            'ip_address' => request()->ip(),
            'user_agent' => request()->userAgent(),
            'timestamp' => now()->toISOString(),
        ];
        
        if ($oldData) {
            $logData['old_data'] = json_encode($oldData);
        }
        
        if ($newData) {
            $logData['new_data'] = json_encode($newData);
        }
        
        Log::channel('product_activities')->info('Product activity', $logData);
    }

}