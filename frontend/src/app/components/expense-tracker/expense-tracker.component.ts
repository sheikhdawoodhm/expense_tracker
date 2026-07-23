import { Component, signal, computed, inject, OnInit, effect } from '@angular/core'; 
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LedgerService, TrackerItem, TrackerType } from '../../services/ledger.service'; 
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-expense-tracker',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './expense-tracker.component.html',
})
export class ExpenseTrackerComponent implements OnInit {
  private ledgerService = inject(LedgerService); 
  private toastr = inject(ToastrService);

  // State Signals
  activeType = signal<TrackerType>('expense');
  isEditing = signal<boolean>(false);
  editingId = signal<number | null>(null);

  // Custom Category State
  showCustomInput = false;
  newCategoryName = '';

  categoriesMap = signal<{ [key in TrackerType]: string[] }>({
    expense: ['Food', 'Rent', 'Utilities', 'Entertainment'],
    asset: ['Stocks', 'Savings Account', 'Real Estate', 'Crypto'],
    liability: ['Credit Card', 'Mortgage', 'Student Loan', 'Car Loan']
  });

  // Dynamic Computed Signals
  currentCategories = computed(() => this.categoriesMap()[this.activeType()]);
  items = this.ledgerService.items;

  // Real-time Net Balance calculation across loaded items
  netBalance = computed(() => {
    return this.items().reduce((acc, item) => {
      if (item.type === 'asset') return acc + Number(item.amount);
      return acc - Number(item.amount);
    }, 0);
  });

  formData = {
    title: '',
    amount: 0,
    category: 'Food'
  };

  constructor() {
    // Extract unique custom categories from the historical DB items dynamically
    effect(() => {
      const items = this.items();
      if (!items || items.length === 0) return;
      
      const map = { ...this.categoriesMap() };
      let changed = false;

      for (const item of items) {
        if (map[item.type] && !map[item.type].includes(item.category)) {
          map[item.type] = [...map[item.type], item.category];
          changed = true;
        }
      }

      if (changed) {
        this.categoriesMap.set(map);
        
        // Safety fallback: If active category isn't in current list, pick first
        if (!map[this.activeType()].includes(this.formData.category)) {
          this.formData.category = map[this.activeType()][0];
        }
      }
    }, { allowSignalWrites: true });
  }

  ngOnInit(): void {
    // Initial fetch from FastAPI on mount
    this.ledgerService.loadItems().subscribe();
  }

  changeType(type: TrackerType) {
    this.activeType.set(type);
    this.formData.category = this.categoriesMap()[type][0];
    this.showCustomInput = false;
  }

  addCustomCategory() {
    const trimmed = this.newCategoryName.trim();
    if (!trimmed) return;

    const formattedCategory = trimmed.charAt(0).toUpperCase() + trimmed.slice(1);
    const currentMap = this.categoriesMap();
    const currentType = this.activeType();

    if (!currentMap[currentType].includes(formattedCategory)) {
      this.categoriesMap.update(prev => ({
        ...prev,
        [currentType]: [...prev[currentType], formattedCategory]
      }));
    }

    this.formData.category = formattedCategory;
    this.newCategoryName = '';
    this.showCustomInput = false;
  }

  saveItem() {
      // Ensure amount is at least valid before sending
      if (this.formData.amount <= 0) {
        this.toastr.warning('Amount must be greater than 0', 'Warning');
        return;
      }

      if (Number(this.formData.amount) >= 900000000000000) {
        this.toastr.warning('Amount exceeds system limits. Please enter a smaller realistic amount.', 'Warning');
        return;
      }

      const payload = {
        title: this.formData.title,
        amount: Number(this.formData.amount),
        type: this.activeType(),
        category: this.formData.category,
        date: new Date().toISOString()
      };

      if (this.isEditing() && this.editingId() !== null) {
        this.ledgerService.updateItem(this.editingId()!, payload).subscribe(() => {
          this.toastr.success('Item updated successfully', 'Success');
          this.resetForm();
        });
      } else {
        this.ledgerService.addItem(payload).subscribe(() => {
          this.toastr.success('Item added successfully', 'Success');
          this.resetForm();
        });
      }
    }

    editItem(item: TrackerItem) {
      this.isEditing.set(true);
      this.editingId.set(item.id);
      this.activeType.set(item.type);
      this.formData = {
        // Handles either field name returned by your service
        title: item.title || (item as any).description || '',
        amount: item.amount,
        category: item.category
      };
    }

 

  deleteItem(id: number) {
    this.ledgerService.deleteItem(id).subscribe(() => {
      this.toastr.success('Item deleted successfully', 'Success');
      if (this.editingId() === id) this.resetForm();
    });
  }

  resetForm() {
    this.isEditing.set(false);
    this.editingId.set(null);
    this.showCustomInput = false;
    this.formData = { 
      title: '', 
      amount: 0, 
      category: this.categoriesMap()[this.activeType()][0]
    };
  }
}